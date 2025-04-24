import json
import pytest

from click.testing import CliRunner
from unittest import mock

from mapbox_tilesets.scripts.cli import (
    publish_changesets,
    view_changeset,
    delete_changeset,
    upload_changeset,
)
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
@mock.patch("requests.Session.post")
def test_cli_publish_changesets_successful(mock_request_post):
    runner = CliRunner()

    # sends expected request
    mock_request_post.return_value = MockResponse(
        {"message": "mock message", "jobId": "1234fakejob"}, 200
    )
    result = runner.invoke(
        publish_changesets, ["test.id", "tests/fixtures/changeset-payload.json"]
    )
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/publish-changesets?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K",
        json={
            "layers": {
                "trees": {
                    "changeset": "mapbox://tileset-changeset/test.id/test-changeset-id"
                }
            }
        },
    )
    assert result.exit_code == 0
    print(result.output)
    assert '{"message": "mock message", "jobId": "1234fakejob"}' in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.post")
def test_cli_publish_changesets_error(mock_request_post):
    runner = CliRunner()

    # sends expected request
    mock_request_post.return_value = MockResponse(
        {"message": "Mock failure message for publishing changeset"},
        400,
    )
    result = runner.invoke(
        publish_changesets, ["test.id", "tests/fixtures/changeset-payload.json"]
    )
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/publish-changesets?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K",
        json={
            "layers": {
                "trees": {
                    "changeset": "mapbox://tileset-changeset/test.id/test-changeset-id"
                }
            }
        },
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    print(result.output)
    assert (
        clean_runner_output(result.output)
        == '{"message": "Mock failure message for publishing changeset"}'
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_view_changeset(mock_request_get, MockResponse):
    message = {"id": "mapbox://tileset-changeset/test-user/hello-world-changeset"}
    mock_request_get.return_value = MockResponse(message, status_code=200)
    runner = CliRunner()
    result = runner.invoke(view_changeset, ["test-user", "hello-world-changeset"])

    assert result.exit_code == 0
    assert json.loads(result.output) == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.delete")
def test_cli_delete_changeset(mock_request_delete, MockResponse):
    mock_request_delete.return_value = MockResponse("", status_code=204)
    runner = CliRunner()
    result = runner.invoke(
        delete_changeset,
        ["test-user", "hello-world-changeset"],
        input="test-user/hello-world-changeset",
    )

    assert result.exit_code == 0
    assert (
        result.output
        == 'To confirm changeset deletion please enter the full changeset id "test-user/hello-world-changeset": test-user/hello-world-changeset\nChangeset deleted.\n'
    )
    force_result = runner.invoke(
        delete_changeset, ["test-user", "hello-world", "--force"]
    )
    assert force_result.exit_code == 0
    assert force_result.output == "Changeset deleted.\n"


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.delete")
def test_cli_delete_changeset_aborted(mock_request_delete, MockResponse):
    mock_request_delete.return_value = MockResponse("", status_code=201)
    runner = CliRunner()
    result = runner.invoke(
        delete_changeset, ["test-user", "hello-world-changeset"], input="wrong/id"
    )
    assert result.exit_code == 1
    assert (
        result.output
        == 'To confirm changeset deletion please enter the full changeset id "test-user/hello-world-changeset": wrong/id\nError: wrong/id does not match test-user/hello-world-changeset. Aborted!\n'
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoder")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoderMonitor")
@mock.patch("requests.Session.post")
def test_cli_upload_changeset(
    mock_request_post,
    mock_multipart_encoder_monitor,
    mock_multipart_encoder,
    MockResponse,
    MockMultipartEncoding,
):
    okay_response = {
        "id": "mapbox://tileset-changeset/test-user/populated-places-source"
    }
    mock_request_post.return_value = MockResponse(okay_response, status_code=200)

    expected_json = b'{"id":1,"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]},"properties":{"name":"Dinagat Islands"}}\n{"id":2,"type":"Feature","geometry":{"type":"Point","coordinates":[-76.971938,38.921387]},"properties":{"name":"ZELALEM INJERA"}}\n{"id":3,"delete":true}\n'

    def side_effect(fields):
        assert fields["file"][1].read() == expected_json
        return MockMultipartEncoding()

    mock_multipart_encoder.side_effect = side_effect

    runner = CliRunner()
    validated_result = runner.invoke(
        upload_changeset,
        [
            "test-user",
            "populated-places-source",
            "tests/fixtures/valid-changeset.ldgeojson",
        ],
    )
    assert validated_result.exit_code == 0
    assert (
        validated_result.output
        == """upload progress\n{"id": "mapbox://tileset-changeset/test-user/populated-places-source"}\n"""
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoder")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoderMonitor")
@mock.patch("requests.Session.put")
def test_cli_upload_changeset_replace(
    mock_request_post,
    mock_multipart_encoder_monitor,
    mock_multipart_encoder,
    MockResponse,
    MockMultipartEncoding,
):
    okay_response = {"id": "mapbox://tileset-changeset/test-user/hello-world"}
    mock_request_post.return_value = MockResponse(okay_response, status_code=200)

    expected_json = b'{"id":1,"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]},"properties":{"name":"Dinagat Islands"}}\n{"id":2,"type":"Feature","geometry":{"type":"Point","coordinates":[-76.971938,38.921387]},"properties":{"name":"ZELALEM INJERA"}}\n{"id":3,"delete":true}\n'

    def side_effect(fields):
        assert fields["file"][1].read() == expected_json
        return MockMultipartEncoding()

    mock_multipart_encoder.side_effect = side_effect

    runner = CliRunner()
    validated_result = runner.invoke(
        upload_changeset,
        [
            "test-user",
            "hello-world",
            "tests/fixtures/valid-changeset.ldgeojson",
            "--replace",
        ],
    )
    assert validated_result.exit_code == 0

    assert (
        validated_result.output
        == """upload progress\n{"id": "mapbox://tileset-changeset/test-user/hello-world"}\n"""
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoder")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoderMonitor")
@mock.patch("requests.Session.post")
def test_cli_upload_source_invalid_changeset(
    mock_request_post,
    mock_multipart_encoder,
    MockResponse,
    MockMultipartEncoding,
):
    expected_json = b'{"id":1,"delete":true,"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]},"properties":{"name":"Dinagat Islands"}}\n{"id":2,"delete":false}\n'

    def side_effect(fields):
        assert fields["file"][1].read() == expected_json
        return MockMultipartEncoding()

    mock_multipart_encoder.side_effect = side_effect

    runner = CliRunner()
    validated_result = runner.invoke(
        upload_changeset,
        [
            "test-user",
            "populated-places-source",
            "tests/fixtures/invalid-changeset.ldgeojson",
        ],
    )

    assert validated_result.exit_code == 1


@pytest.mark.usefixtures("token_environ")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoder")
@mock.patch("mapbox_tilesets.scripts.cli.MultipartEncoderMonitor")
@mock.patch("requests.Session.post")
def test_cli_upload_changeset_no_validation(
    mock_request_post,
    mock_multipart_encoder_monitor,
    mock_multipart_encoder,
    MockResponse,
    MockMultipartEncoding,
):
    okay_response = {"id": "mapbox://tileset-changeset/test-user/hello-world"}
    mock_request_post.return_value = MockResponse(okay_response, status_code=200)

    expected_json = b'{"id":1,"delete":true,"type":"Feature","geometry":{"type":"Point","coordinates":[125.6,10.1]},"properties":{"name":"Dinagat Islands"}}\n{"id":2,"delete":false}\n'

    def side_effect(fields):
        assert fields["file"][1].read() == expected_json
        return MockMultipartEncoding()

    mock_multipart_encoder.side_effect = side_effect

    runner = CliRunner()
    validated_result = runner.invoke(
        upload_changeset,
        [
            "test-user",
            "hello-world",
            "tests/fixtures/invalid-changeset-geojson.ldgeojson",
            "--no-validation",
        ],
    )
    assert validated_result.exit_code == 0

    assert (
        validated_result.output
        == """upload progress\n{"id": "mapbox://tileset-changeset/test-user/hello-world"}\n"""
    )
