import json
import os
from unittest import mock

import click
import pytest
from click.testing import CliRunner
from utils import clean_runner_output

from mapbox_tilesets.scripts.cli import (
    delete_source,
    list_sources,
    upload_source,
    validate_source,
    view_source,
)


@pytest.mark.usefixtures("token_environ")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoder")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoderMonitor")
@mock.patch("requests.Session.put")
def test_cli_upload_source_replace(
    mock_request_put,
    mock_multipart_encoder_monitor,
    mock_multipart_encoder,
    MockResponse,
    MockMultipartEncoding,
):
    okay_response = {"id": "mapbox://tileset-source/test-user/hello-world"}
    mock_request_put.return_value = MockResponse(okay_response, status_code=200)

    expected_json = b'{"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]},"properties":{"name":"Dinagat Islands"}}\n'

    def side_effect(fields):
        assert fields["file"][1].read() == expected_json
        return MockMultipartEncoding()

    mock_multipart_encoder.side_effect = side_effect

    runner = CliRunner()
    validated_result = runner.invoke(
        upload_source,
        ["test-user", "hello-world", "tests/fixtures/valid.ldgeojson", "--replace"],
    )
    assert validated_result.exit_code == 0
    assert (
        validated_result.output
        == """upload progress\n{"id": "mapbox://tileset-source/test-user/hello-world"}\n"""
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoder")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoderMonitor")
@mock.patch("requests.Session.put")
def test_cli_upload_source_no_replace(
    mock_request_post,
    mock_multipart_encoder_monitor,
    mock_multipart_encoder,
    MockResponse,
    MockMultipartEncoding,
):
    okay_response = {"id": "mapbox://tileset-source/test-user/hello-world"}
    mock_request_post.return_value = MockResponse(okay_response, status_code=200)

    expected_json = b'{"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]},"properties":{"name":"Dinagat Islands"}}\n'

    def side_effect(fields):
        assert fields["file"][1].read() == expected_json
        return MockMultipartEncoding()

    mock_multipart_encoder.side_effect = side_effect

    runner = CliRunner()
    validated_result = runner.invoke(
        upload_source,
        ["test-user", "hello-world", "tests/fixtures/valid.ldgeojson", "--replace"],
    )
    assert validated_result.exit_code == 0

    assert (
        validated_result.output
        == """upload progress\n{"id": "mapbox://tileset-source/test-user/hello-world"}\n"""
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoder")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoderMonitor")
@mock.patch("requests.Session.post")
def test_cli_upload_source(
    mock_request_post,
    mock_multipart_encoder_monitor,
    mock_multipart_encoder,
    MockResponse,
    MockMultipartEncoding,
):
    okay_response = {"id": "mapbox://tileset-source/test-user/populated-places-source"}
    mock_request_post.return_value = MockResponse(okay_response, status_code=200)

    expected_json = b'{"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]},"properties":{"name":"Dinagat Islands"}}\n'

    def side_effect(fields):
        assert fields["file"][1].read() == expected_json
        return MockMultipartEncoding()

    mock_multipart_encoder.side_effect = side_effect

    runner = CliRunner()
    validated_result = runner.invoke(
        upload_source,
        ["test-user", "populated-places-source", "tests/fixtures/valid.ldgeojson"],
    )
    assert validated_result.exit_code == 0
    assert (
        validated_result.output
        == """upload progress\n{"id": "mapbox://tileset-source/test-user/populated-places-source"}\n"""
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoder")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoderMonitor")
@mock.patch("requests.Session.post")
def test_cli_upload_source_invalid_polygon(
    mock_request_post,
    mock_multipart_encoder,
    MockResponse,
    MockMultipartEncoding,
):
    expected_json = b'{"type":"Feature","id":"01","geometry":{"type":"Polygon","coordinates":[[-150.957,-40.5948],[-155,-41],[-152,-42],[-152,-40]]},"properties":{"name":"Ducky Loo"}}\n'

    def side_effect(fields):
        assert fields["file"][1].read() == expected_json
        return MockMultipartEncoding()

    mock_multipart_encoder.side_effect = side_effect

    runner = CliRunner()
    validated_result = runner.invoke(
        upload_source,
        [
            "test-user",
            "populated-places-source",
            "tests/fixtures/invalid-polygon.ldgeojson",
        ],
    )
    assert validated_result.exit_code == 1

    assert (
        clean_runner_output(validated_result.output)
        == "Error in feature number 0: Each linear ring must end where it started"
    )


@pytest.mark.usefixtures("token_environ")
def validate_source_id(self):
    self.assertRaises(
        click.BadParameter,
        value="mapbox://tileset-source/test-user/hello-world",
        param=None,
        ctx=None,
    )
    self.assertEqual("hello-world", value="hello-world", param=None, ctx=None)


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
