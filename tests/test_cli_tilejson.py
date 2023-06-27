import json
import pytest
from unittest import mock
from click.testing import CliRunner
from mapbox_tilesets.scripts.cli import tilejson
from utils import clean_runner_output


class MockResponse:
    def __init__(self, mock_json, status_code):
        self.text = json.dumps(mock_json)
        self._json = mock_json
        self.status_code = status_code

    def MockResponse(self):
        return self

    def json(self):
        return self._json


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_tilejson(mock_request_get, MockResponse):
    runner = CliRunner()

    message = {
        "bounds": [-74.355469, 40.446947, -73.652344, 40.979898],
        "center": [-74.003906, 40.713423, 0],
        "created": 111,
        "filesize": 111,
        "format": "pbf",
        "id": "test.id",
        "mapbox_logo": True,
        "maxzoom": 16,
        "minzoom": 0,
        "modified": 111,
        "name": "Test ID TileJSON",
        "private": True,
        "scheme": "xyz",
        "tilejson": "2.2.0",
        "tiles": [
            "http://api.mapbox.com/v4/test.id/{z}/{x}/{y}.vector.pbf?access_token=test-token"
        ],
        "vector_layers": [{"fields": {"waka": "string"}}],
        "webpage": "http://api.mapbox.com/v4/test.id/page.html?access_token=test-token",
    }
    # sends expected request
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(tilejson, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/v4/test.id.json?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 0


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_tilejson_composite(mock_request_get, MockResponse):
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse("")
    result = runner.invoke(tilejson, ["test.id,test.another"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/v4/test.id,test.another.json?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 0


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_tilejson_secure(mock_request_get, MockResponse):
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse("")
    result = runner.invoke(tilejson, ["test.id", "--secure"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/v4/test.id.json?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&secure"
    )
    assert result.exit_code == 0


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_tilejson_error(mock_request_get, MockResponse):
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse({"message": "uh oh"}, 422)
    result = runner.invoke(tilejson, ["test.id,test.another"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/v4/test.id,test.another.json?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)


@pytest.mark.usefixtures("token_environ")
def test_cli_tilejson_invalid_tileset_id():
    runner = CliRunner()

    # sends expected request
    result = runner.invoke(tilejson, ["invalid@@id"])
    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert clean_runner_output(result.output) == "Invalid Tileset ID"
