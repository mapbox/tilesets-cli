from click.testing import CliRunner
from unittest import mock
import json

import pytest

from tilesets.cli import (
    add_source,
    view_source,
    delete_source,
    validate_source,
    list_sources,
)


class MockResponse:
    def __init__(self, mock_text, status_code):
        self.text = mock_text
        self.status_code = status_code

    def MockResponse(self):
        return self

    def json(self):
        return json.loads(self.text)


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.post")
def test_cli_add_source(mock_request_post):
    mock_request_post.return_value = MockResponse(
        '{"id":"mapbox://tileset-source/test-user/hello-world"}', 200
    )
    runner = CliRunner()
    result = runner.invoke(
        add_source, ["test-user", "hello-world", "tests/fixtures/valid.ldgeojson"]
    )
    assert result.exit_code == 0
    assert "Validating tests/fixtures/valid.ldgeojson ...\n✔ valid" in result.output
    assert (
        "Adding tests/fixtures/valid.ldgeojson to mapbox://tileset-source/test-user/hello-world"
        in result.output
    )
    assert (
        '{\n  "id": "mapbox://tileset-source/test-user/hello-world"\n}\n'
        in result.output
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_view_source(mock_request_get):
    mock_request_get.return_value = MockResponse(
        '{"id":"mapbox://tileset-source/test-user/hello-world"}', 200
    )
    runner = CliRunner()
    result = runner.invoke(view_source, ["test-user", "hello-world"])
    assert result.exit_code == 0
    assert (
        result.output
        == '{\n  "id": "mapbox://tileset-source/test-user/hello-world"\n}\n'
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.delete")
def test_cli_delete_source(mock_request_delete):
    mock_request_delete.return_value = MockResponse("", 201)
    runner = CliRunner()
    result = runner.invoke(delete_source, ["test-user", "hello-world"])
    assert result.exit_code == 0
    assert result.output == "Source deleted.\n"


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_view_source(mock_request_get):
    mock_request_get.return_value = MockResponse(
        '[{"id":"mapbox://tileset-source/test-user/hello-world"},\
        {"id":"mapbox://tileset-source/test-user/hola-mundo"}]',
        200,
    )
    runner = CliRunner()
    result = runner.invoke(list_sources, ["test-user"])
    assert result.exit_code == 0
    assert "mapbox://tileset-source/test-user/hello-world" in result.output
    assert "mapbox://tileset-source/test-user/hola-mundo" in result.output


@pytest.mark.usefixtures("token_environ")
def test_cli_validate_source():
    runner = CliRunner()
    result = runner.invoke(validate_source, ["tests/fixtures/valid.ldgeojson"])
    assert result.exit_code == 0
    assert result.output == "Validating tests/fixtures/valid.ldgeojson ...\n✔ valid\n"
