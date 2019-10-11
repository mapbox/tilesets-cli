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
    message = {"id": "mapbox://tileset-source/test-user/hello-world"}
    mock_request_post.return_value = MockResponse(message, status_code=200)
    runner = CliRunner()
    result = runner.invoke(
        add_source, ["test-user", "hello-world", "tests/fixtures/valid.ldgeojson"]
    )
    assert result.exit_code == 0

    assert (
        result.output == """{"id": "mapbox://tileset-source/test-user/hello-world"}\n"""
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.post")
def test_cli_add_source_dryrun(mock_request_post, MockResponse):
    message = {"id": "mapbox://tileset-source/test-user/hello-world"}
    mock_request_post.return_value = MockResponse(message, status_code=200)
    runner = CliRunner()
    result = runner.invoke(
        add_source,
        ["--dryrun", "test-user", "hello-world", "tests/fixtures/valid.ldgeojson"],
    )
    assert not mock_request_post.called

    assert result.exit_code == 0

    assert (
        result.output
        == """[DRYRUN] Adding 1 features to https://api.mapbox.com/tilesets/v1/sources/test-user/hello-world\n"""
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
    result = runner.invoke(delete_source, ["test-user", "hello-world"])
    assert result.exit_code == 0
    assert result.output == "Source deleted.\n"


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
