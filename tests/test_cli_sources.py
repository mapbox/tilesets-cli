from click.testing import CliRunner
from unittest import mock
import json

import pytest

from tilesets.scripts.cli import (
    add_source,
    view_source,
    delete_source,
    validate_source,
    list_sources,
)


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.post")
def test_cli_add_source(mock_request_post, MockResponse):
    okay_response = {"id": "mapbox://tileset-source/test-user/hello-world"}
    mock_request_post.return_value = MockResponse(okay_response, status_code=200)
    runner = CliRunner()
    validated_result = runner.invoke(
        add_source, ["test-user", "hello-world", "tests/fixtures/valid.ldgeojson"]
    )
    assert validated_result.exit_code == 0

    assert (
        validated_result.output
        == """{"id": "mapbox://tileset-source/test-user/hello-world"}\n"""
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.post")
def test_cli_add_source_no_validation(mock_request_post, MockResponse):
    error_response = {
        "message": "Invalid file format. Only GeoJSON features are allowed."
    }
    mock_request_post.return_value = MockResponse(error_response, status_code=400)
    runner = CliRunner()
    no_validation_result = runner.invoke(
        add_source,
        [
            "test-user",
            "hello-again",
            "tests/fixtures/invalid.ldgeojson",
            "--no-validation",
        ],
    )
    assert no_validation_result.exit_code == 1

    assert (
        no_validation_result.exception.message
        == '{"message": "Invalid file format. Only GeoJSON features are allowed."}'
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_view_source(mock_request_get, MockResponse):
    message = {"id": "mapbox://tileset-source/test-user/hello-world"}
    mock_request_get.return_value = MockResponse(message, status_code=200)
    runner = CliRunner()
    result = runner.invoke(view_source, ["test-user", "hello-world"])

    assert result.exit_code == 0
    assert json.loads(result.output) == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.delete")
def test_cli_delete_source(mock_request_delete, MockResponse):
    mock_request_delete.return_value = MockResponse("", status_code=201)
    runner = CliRunner()
    result = runner.invoke(delete_source, ["test-user", "hello-world"], input="y")
    assert result.exit_code == 0
    assert (
        result.output
        == "Are you sure you want to delete test-user hello-world? [y/N]: y\nSource deleted.\n"
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.delete")
def test_cli_delete_source_aborted(mock_request_delete, MockResponse):
    mock_request_delete.return_value = MockResponse("", status_code=201)
    runner = CliRunner()
    result = runner.invoke(delete_source, ["test-user", "hello-world"], input="n")
    assert result.exit_code == 1
    assert (
        result.output
        == "Are you sure you want to delete test-user hello-world? [y/N]: n\nAborted!\n"
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_view_source_2(mock_request_get, MockResponse):
    message = [
        {"id": "mapbox://tileset-source/test-user/hello-world"},
        {"id": "mapbox://tileset-source/test-user/hola-mundo"},
    ]
    mock_request_get.return_value = MockResponse(message, status_code=200)
    runner = CliRunner()
    result = runner.invoke(list_sources, ["test-user"])

    assert result.exit_code == 0
    assert (
        result.output
        == "mapbox://tileset-source/test-user/hello-world\nmapbox://tileset-source/test-user/hola-mundo\n"
    )


@pytest.mark.usefixtures("token_environ")
def test_cli_validate_source():
    runner = CliRunner()
    result = runner.invoke(validate_source, ["tests/fixtures/valid.ldgeojson"])
    assert result.exit_code == 0
    assert result.output == "Validating features\n✔ valid\n"
