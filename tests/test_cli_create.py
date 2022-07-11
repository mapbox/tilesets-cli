import json

from unittest import mock

from click.testing import CliRunner
import pytest

from mapbox_tilesets.scripts.cli import create


@pytest.mark.usefixtures("token_environ")
def test_cli_create_missing_recipe():
    runner = CliRunner()
    # missing --recipe option
    result = runner.invoke(create, ["test.id"])
    assert result.exit_code == 2
    assert "Missing option '--recipe' / '-r'" in result.output


@pytest.mark.usefixtures("token_environ")
def test_cli_create_missing_name():
    runner = CliRunner()
    # missing --name option
    result = runner.invoke(
        create, ["test.id", "--recipe", "tests/fixtures/recipe.json"]
    )
    assert result.exit_code == 2
    assert "Missing option '--name'" in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.post")
def test_cli_create_success(mock_request_post, MockResponse):
    runner = CliRunner()
    # sends request to proper endpoints
    message = {"message": "mock message"}

    mock_request_post.return_value = MockResponse(message)
    result = runner.invoke(
        create,
        [
            "test.id",
            "--recipe",
            "tests/fixtures/recipe.json",
            "--name",
            "test name",
            '--attribution=[{"text":"natural earth data","link":"https://naturalearthdata.com"}]',
            "--privacy=private",
        ],
    )
    assert result.exit_code == 0
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K",
        json={
            "name": "test name",
            "description": "",
            "recipe": {"minzoom": 0, "maxzoom": 10, "layer_name": "test_layer"},
            "attribution": [
                {"text": "natural earth data", "link": "https://naturalearthdata.com"}
            ],
            "private": True,
        },
    )
    assert json.loads(result.output) == message


@pytest.mark.usefixtures("token_environ")
def test_cli_create_attribution_json_parse_error():
    runner = CliRunner()
    # sends request to proper endpoints
    result = runner.invoke(
        create,
        [
            "test.id",
            "--recipe",
            "tests/fixtures/recipe.json",
            "--name",
            "test name",
            "--attribution",
            "not valid json",
        ],
    )

    assert result.exit_code == 1
    assert "Unable to parse attribution JSON" in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.post")
def test_cli_create_success_description(mock_request_post, MockResponse):
    runner = CliRunner()
    # sends request with "description" included

    message = {"message": "mock message with description"}
    mock_request_post.return_value = MockResponse(message)
    result = runner.invoke(
        create,
        [
            "test.id",
            "--recipe",
            "tests/fixtures/recipe.json",
            "--name",
            "test name",
            "--description",
            "test description",
        ],
    )
    assert result.exit_code == 0

    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K",
        json={
            "name": "test name",
            "description": "test description",
            "recipe": {"minzoom": 0, "maxzoom": 10, "layer_name": "test_layer"},
        },
    )
    assert json.loads(result.output) == {"message": "mock message with description"}


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.post")
def test_cli_create_private_invalid(mock_request_post, MockResponse):
    runner = CliRunner()
    # sends request with "description" included
    mock_request_post.return_value = MockResponse(
        '{"message":"mock message with description"}'
    )
    result = runner.invoke(
        create,
        [
            "test.id",
            "--recipe",
            "tests/fixtures/recipe.json",
            "--name",
            "test name",
            "--privacy",
            "invalid-privacy-value",
        ],
    )
    assert result.exit_code == 2
    assert (
        "Error: Invalid value for '--privacy' / '-p': 'invalid-privacy-value' is not one of 'public', 'private'."
        in result.output
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.post")
def test_cli_use_token_flag(mock_request_post, MockResponse):
    runner = CliRunner()
    message = {"message": "mock message"}
    mock_request_post.return_value = MockResponse(message)
    # Provides the flag --token
    result = runner.invoke(
        create,
        [
            "test.id",
            "--recipe",
            "tests/fixtures/recipe.json",
            "--name",
            "test name",
            "--token",
            "flag-token",
        ],
    )
    assert result.exit_code == 0
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id?access_token=flag-token",
        json={
            "name": "test name",
            "description": "",
            "recipe": {"minzoom": 0, "maxzoom": 10, "layer_name": "test_layer"},
        },
    )
    assert json.loads(result.output) == message
