import json
import pytest

from click.testing import CliRunner
from unittest import mock

from mapbox_tilesets.scripts.cli import validate_recipe


class MockResponse:
    def __init__(self, mock_text):
        self.text = mock_text
        self.status_code = 200

    def MockResponse(self):
        return self


@pytest.mark.usefixtures("token_environ")
def test_cli_validate_recipe_no_recipe():
    runner = CliRunner()
    result = runner.invoke(validate_recipe, ["does/not/exist/recipe.json"])
    assert result.exit_code == 2
    assert "Path 'does/not/exist/recipe.json' does not exist" in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.put")
def test_cli_validate_recipe(mock_request_put, MockResponse):
    runner = CliRunner()

    # sends expected request
    message = {"message": "mock message"}
    mock_request_put.return_value = MockResponse(message)
    result = runner.invoke(validate_recipe, ["tests/fixtures/recipe.json"])
    mock_request_put.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/validateRecipe?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K",
        json={"minzoom": 0, "maxzoom": 10, "layer_name": "test_layer"},
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.put")
def test_cli_validate_recipe_use_token_flag(mock_request_put, MockResponse):
    runner = CliRunner()
    message = {"message": "mock message"}
    mock_request_put.return_value = MockResponse(message)
    # Provides the flag --token
    result = runner.invoke(
        validate_recipe, ["tests/fixtures/recipe.json", "--token", "flag-token"]
    )
    mock_request_put.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/validateRecipe?access_token=flag-token",
        json={"minzoom": 0, "maxzoom": 10, "layer_name": "test_layer"},
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == message
