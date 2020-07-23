from click.testing import CliRunner
import json
import os
from unittest import mock

import pytest

from mapbox_tilesets.scripts.cli import (
    add_source,
    view_source,
    delete_source,
    validate_source,
    list_sources,
)


@pytest.mark.usefixtures("token_environ")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoder")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoderMonitor")
@mock.patch("requests.Session.post")
def test_cli_add_source(mock_request_post, mock_multipart_encoder_monitor, mock_multipart_encoder, MockResponse, MockMultipartEncoding):
    okay_response = {"id": "mapbox://tileset-source/test-user/hello-world"}
    mock_request_post.return_value = MockResponse(okay_response, status_code=200)

    expected_json = b'{"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]},"properties":{"name":"Dinagat Islands"}}\n'
    def side_effect(fields):
        assert fields['file'][1].read() == expected_json
        return MockMultipartEncoding()
    mock_multipart_encoder.side_effect = side_effect

    runner = CliRunner()
    validated_result = runner.invoke(
        add_source, ["test-user", "hello-world", "tests/fixtures/valid.ldgeojson"]
    )
    assert validated_result.exit_code == 0

    assert (
        validated_result.output
        == """{"id": "mapbox://tileset-source/test-user/hello-world"}\n"""
    )


def test_cli_add_source_no_token():
    if "MAPBOX_ACCESS_TOKEN" in os.environ:
        del os.environ["MAPBOX_ACCESS_TOKEN"]
    if "MapboxAccessToken" in os.environ:
        del os.environ["MapboxAccessToken"]

    runner = CliRunner()
    unauthenticated_result = runner.invoke(
        add_source, ["test-user", "hello-world", "tests/fixtures/valid.ldgeojson"]
    )
    assert unauthenticated_result.exit_code == 1

    assert (
        str(unauthenticated_result.exception)
        == """No access token provided. Please set the MAPBOX_ACCESS_TOKEN environment variable or use the --token flag."""
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.post")
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
@mock.patch("requests.Session.get")
def test_cli_view_source(mock_request_get, MockResponse):
    message = {"id": "mapbox://tileset-source/test-user/hello-world"}
    mock_request_get.return_value = MockResponse(message, status_code=200)
    runner = CliRunner()
    result = runner.invoke(view_source, ["test-user", "hello-world"])

    assert result.exit_code == 0
    assert json.loads(result.output) == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.delete")
def test_cli_delete_source(mock_request_delete, MockResponse):
    mock_request_delete.return_value = MockResponse("", status_code=204)
    runner = CliRunner()
    result = runner.invoke(
        delete_source, ["test-user", "hello-world"], input="test-user/hello-world"
    )
    assert result.exit_code == 0
    assert (
        result.output
        == 'To confirm source deletion please enter the full source id "test-user/hello-world": test-user/hello-world\nSource deleted.\n'
    )
    force_result = runner.invoke(delete_source, ["test-user", "hello-world", "--force"])
    assert force_result.exit_code == 0
    assert force_result.output == "Source deleted.\n"


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.delete")
def test_cli_delete_source_aborted(mock_request_delete, MockResponse):
    mock_request_delete.return_value = MockResponse("", status_code=201)
    runner = CliRunner()
    result = runner.invoke(
        delete_source, ["test-user", "hello-world"], input="wrong/id"
    )
    assert result.exit_code == 1
    assert (
        result.output
        == 'To confirm source deletion please enter the full source id "test-user/hello-world": wrong/id\nError: wrong/id does not match test-user/hello-world. Aborted!\n'
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
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
