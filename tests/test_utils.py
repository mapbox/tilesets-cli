import os
import pytest
import json
from mapbox_tilesets.utils import (
    _get_api,
    _get_session,
    _get_token,
    geojson_validate,
    validate_tileset_id,
    _convert_precision_to_zoom,
    calculate_tiles_area,
)
from mapbox_tilesets.errors import TilesetsError


def test_get_api():
    api = _get_api()
    assert api == "https://api.mapbox.com"
    os.environ["MAPBOX_API"] = "https://different.com"
    api = _get_api()
    assert api == "https://different.com"


def test_get_session():
    s = _get_session("my_application", "1.0.0")
    assert "user-agent" in s.headers
    assert s.headers["user-agent"] == "my_application/1.0.0"


def test_get_token_parameter():
    token = "token-parameter"
    assert token == _get_token(token)


def test_get_token_environment_variables():
    token1 = "token-environ1"
    token2 = "token-environ2"
    os.environ["MAPBOX_ACCESS_TOKEN"] = token1
    assert token1 == _get_token()
    del os.environ["MAPBOX_ACCESS_TOKEN"]
    os.environ["MapboxAccessToken"] = token2
    assert token2 == _get_token()
    del os.environ["MapboxAccessToken"]


def test_get_token_errors_without_token():
    with pytest.raises(TilesetsError) as excinfo:
        _get_token()

    assert (
        str(excinfo.value)
        == "No access token provided. Please set the MAPBOX_ACCESS_TOKEN environment variable or use the --token flag."
    )


def test_validate_tileset_id():
    tileset = "iama.test"

    assert validate_tileset_id(tileset)


def test_validate_tileset_id_badfmt():
    tileset = "iama.test.ok"

    assert not validate_tileset_id(tileset)


def test_validate_tileset_id_toolong():
    tileset = "hellooooooooooooooooooooooooooooooo.hiiiiiiiuuuuuuuuuuuuuuuuuuuuuu"

    assert not validate_tileset_id(tileset)


def test_geojson_validate():
    geometry = {"type": "Polygon", "coordinates": [[[1, 2], [3, 4], [5, 6]]]}
    with pytest.raises(TilesetsError) as excinfo:
        geojson_validate(2, geometry)

    assert (
        str(excinfo.value)
        == "Error in feature number 2: Each linear ring must contain at least 4 positions"
    )


def test_geojson_validate_open_ring():
    geometry = {"type": "Polygon", "coordinates": [[[1, 2], [3, 4], [5, 6], [7, 8]]]}
    with pytest.raises(TilesetsError) as excinfo:
        geojson_validate(2, geometry)

    assert (
        str(excinfo.value)
        == "Error in feature number 2: Each linear ring must end where it started"
    )


def test_geojson_validate_closed_ring():
    geometry = {"type": "Polygon", "coordinates": [[[1, 2], [3, 4], [5, 6], [1, 2]]]}
    assert geojson_validate(2, geometry) is None


def test_geojson_validate_closed_ring_correct_winding_order():
    geometry = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
    }
    assert geojson_validate(2, geometry) is None


def test_geojson_validate_closed_ring_incorrect_winding_order():
    geometry = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]],
    }
    assert geojson_validate(2, geometry) is None


def test_convert_precision_to_zoom_10m():
    precision = "10m"
    assert _convert_precision_to_zoom(precision) == 6


def test_convert_precision_to_zoom_1m():
    precision = "1m"
    assert _convert_precision_to_zoom(precision) == 11


def test_convert_precision_to_zoom_30cm():
    precision = "30cm"
    assert _convert_precision_to_zoom(precision) == 14


def test_convert_precision_to_zoom_1cm():
    precision = "1cm"
    return _convert_precision_to_zoom(precision) == 17


# area assertions from Mapbox Studio tiled area with zooms specified in recipes
def test_calculate_tiles_area_with_10m_precision():
    filename = "tests/fixtures/precision-testing.ldgeojson"
    f = open(filename)
    features = json.load(f)
    area = round(calculate_tiles_area(features, "10m"))
    assert area == 1485128


def test_calculate_tiles_area_with_1m_precision():
    filename = "tests/fixtures/precision-testing.ldgeojson"
    f = open(filename)
    features = json.load(f)
    area = round(calculate_tiles_area(features, "1m"))
    assert area == 2562


def test_calculate_tiles_area_with_30cm_precision():
    filename = "tests/fixtures/precision-testing.ldgeojson"
    f = open(filename)
    features = json.load(f)
    area = round(calculate_tiles_area(features, "30cm"))
    assert area == 65


def test_calculate_tiles_area_with_1cm_precision():
    filename = "tests/fixtures/precision-testing.ldgeojson"
    f = open(filename)
    features = json.load(f)
    area = round(calculate_tiles_area(features, "1cm"))
    assert area == 2
