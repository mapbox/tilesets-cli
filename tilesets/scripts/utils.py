import os
import click
import json
from json import JSONDecoder
from functools import partial
from jsonschema import validate

tileset_arg = click.argument("tileset", required=True, type=str)


def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


# takes a list of files or directories and converts
# all directories into absolute file paths
def flatten(files):
    for f in files:
        if os.path.isdir(f):
            for dir_file in absoluteFilePaths(f):
                yield dir_file
        else:
            yield f


def print_response(text):
    try:
        j = json.loads(text)
        msg = json.dumps(j, indent=2, sort_keys=True)
        click.echo(msg)
    except:
        click.echo("Failure \n" + text)


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
