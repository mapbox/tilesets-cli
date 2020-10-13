import os
import re

import numpy as np

from jsonschema import validate
from requests import Session
from supermercado.burntiles import burn

import mapbox_tilesets


def _get_token(token=None):
    """Get Mapbox access token from arg or environment"""
    token = (
        token
        or os.environ.get("MAPBOX_ACCESS_TOKEN")
        or os.environ.get("MapboxAccessToken")
    )

    if token is not None:
        return token

    raise mapbox_tilesets.errors.TilesetsError(
        "No access token provided. Please set the MAPBOX_ACCESS_TOKEN environment variable or use the --token flag."
    )


def _get_api():
    """Get Mapbox tileset API base URL from environment"""
    return os.environ.get("MAPBOX_API", "https://api.mapbox.com")


def _get_session(
    application=mapbox_tilesets.__name__, version=mapbox_tilesets.__version__
):
    """Get a configured session"""
    s = Session()
    s.headers.update({"user-agent": "{}/{}".format(application, version)})
    return s


def validate_tileset_id(tileset_id):
    """Assess if a Mapbox tileset_id is valid

    Parameters
    ----------
    tileset_id: str
        tileset_id of the form {account}.{tileset}
        - account and tileset should each be 32 characters or fewer.

    Returns
    -------
    is_valid: bool
        boolean indicating if the tileset_id is valid
    """
    pattern = r"^[a-z0-9-_]{1,32}\.[a-z0-9-_]{1,32}$"

    return re.match(pattern, tileset_id, flags=re.IGNORECASE)


def validate_geojson(feature):
    schema = {
        "definitions": {},
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "http://example.com/root.json",
        "type": "object",
        "title": "GeoJSON Schema",
        "required": ["type", "geometry", "properties"],
        "properties": {
            "type": {
                "$id": "#/properties/type",
                "type": "string",
                "title": "The Type Schema",
                "default": "",
                "examples": ["Feature"],
                "pattern": "^(.*)$",
            },
            "geometry": {
                "$id": "#/properties/geometry",
                "type": "object",
                "title": "The Geometry Schema",
                "required": ["type", "coordinates"],
                "properties": {
                    "type": {
                        "$id": "#/properties/geometry/properties/type",
                        "type": "string",
                        "title": "The Type Schema",
                        "default": "",
                        "examples": ["Point"],
                        "pattern": "^(.*)$",
                    },
                    "coordinates": {
                        "$id": "#/properties/geometry/properties/coordinates",
                        "type": "array",
                        "title": "The Coordinates Schema",
                    },
                },
            },
            "properties": {
                "$id": "#/properties/properties",
                "type": "object",
                "title": "The Properties Schema",
            },
        },
    }

    return validate(instance=feature, schema=schema)


def _convert_precision_to_zoom(precision):
    """Converts precision to zoom level based on the minimum zoom

    Parameters
    ----------
    precision: string
        precision level

    Returns
    -------
        zoom level

    """
    if precision == "10m":
        return 6
    elif precision == "1m":
        return 11
    elif precision == "30cm":
        return 14
    else:
        return 17


def _tile2lng(tile_x, zoom):
    """Returns tile longitude

    Parameters
    ----------
    tile_x: int
        x coordinate
    zoom: int
        zoom level

    Returns
    -------
        longitude
    """
    return ((tile_x / 2 ** zoom) * 360.0) - 180.0


def _tile2lat(tile_y, zoom):
    """Returns tile latitude

    Parameters
    ----------
    tile_y: int
        y coordinate
    zoom: int
        zoom level

    Returns
    -------
        latitude
    """
    n = np.pi - 2 * np.pi * tile_y / 2 ** zoom
    return (180.0 / np.pi) * np.arctan(0.5 * (np.exp(n) - np.exp(-n)))


def _calculate_tile_area(tile):
    """Returns tile area in square kilometers

    Parameters
    ----------
    tile: list
        tile in format [x,y,z]

    Returns
    -------
        area of tile

    """
    EARTH_RADIUS = 6371.0088
    left = np.deg2rad(_tile2lng(tile[:, 0], tile[:, 2]))
    top = np.deg2rad(_tile2lat(tile[:, 1], tile[:, 2]))
    right = np.deg2rad(_tile2lng(tile[:, 0] + 1, tile[:, 2]))
    bottom = np.deg2rad(_tile2lat(tile[:, 1] + 1, tile[:, 2]))
    return (
        (np.pi / np.deg2rad(180))
        * EARTH_RADIUS ** 2
        * np.abs(np.sin(top) - np.sin(bottom))
        * np.abs(left - right)
    )


def calculate_tiles_area(features, precision):
    """Calculates the area of tiles

    Parameters
    ----------
    features: list
        features from GeoJSON sources and coordinates
    precision: string
        precision level

    Returns
    -------
        total area of all tiles in square kilometers
    """
    zoom = _convert_precision_to_zoom(precision)
    tiles = burn(features, zoom)
    return np.sum(_calculate_tile_area(tiles))
