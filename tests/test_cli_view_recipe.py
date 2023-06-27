import json
import pytest

from click.testing import CliRunner
from unittest import mock

from mapbox_tilesets.scripts.cli import view_recipe
from utils import clean_runner_output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_view_recipe(mock_request_get, MockResponse):
    runner = CliRunner()

    # sends expected request
    message = {"fake": "recipe_data"}
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(view_recipe, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/recipe?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_view_recipe_use_token_flag(mock_request_get, MockResponse):
    runner = CliRunner()
    message = {"fake": "recipe_data"}
    mock_request_get.return_value = MockResponse(message)
    # Provides the flag --token
    result = runner.invoke(view_recipe, ["test.id", "--token", "flag-token"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/recipe?access_token=flag-token"
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_view_recipe_raises(mock_request_get, MockResponse):
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse("not found", status_code=404)
    result = runner.invoke(view_recipe, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/recipe?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 1
    assert clean_runner_output(result.output) == '"not found"'
