from click.testing import CliRunner
from unittest import mock
import pytest

from tilesets.scripts.cli import update_recipe


@pytest.mark.usefixtures("token_environ")
def test_cli_update_recipe_no_recipe():
    runner = CliRunner()
    result = runner.invoke(update_recipe, ["test.id", "does/not/exist/recipe.json"])
    assert result.exit_code == 2
    assert 'Path "does/not/exist/recipe.json" does not exist' in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.patch")
def test_cli_update_recipe(mock_request_patch, MockResponse):
    runner = CliRunner()

    # sends expected request
    mock_request_patch.return_value = MockResponse({}, status_code=201)
    result = runner.invoke(update_recipe, ["test.id", "tests/fixtures/recipe.json"])
    mock_request_patch.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/recipe?access_token=fake-token",
        json={"minzoom": 0, "maxzoom": 10, "layer_name": "test_layer"},
    )
    assert result.exit_code == 0


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.patch")
def test_cli_update_recipe2(mock_request_patch, MockResponse):
    runner = CliRunner()

    mock_request_patch.return_value = MockResponse({}, status_code=201)
    # Provides the flag --token
    result = runner.invoke(
        update_recipe,
        ["test.id", "tests/fixtures/recipe.json", "--token", "flag-token"],
    )
    mock_request_patch.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/recipe?access_token=flag-token",
        json={"minzoom": 0, "maxzoom": 10, "layer_name": "test_layer"},
    )
    assert result.exit_code == 0
