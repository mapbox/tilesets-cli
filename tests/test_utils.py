import os
import pytest
from mapbox_tilesets.utils import _get_session, _get_token, validate_tileset_id
from mapbox_tilesets.errors import TilesetsError


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
