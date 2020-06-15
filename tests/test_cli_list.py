import json
import pytest

from unittest import mock

from click.testing import CliRunner

from mapbox_tilesets.scripts.cli import list


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]
    # sends expected request
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_verbose(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]
    # sends expected request
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--verbose"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=fake-token"
    )
    assert result.exit_code == 0

    assert [
        json.loads(tileset.strip()) for tileset in result.output.split("\n") if tileset
    ] == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_bad_token(mock_request_get, MockResponse):
    runner = CliRunner()

    message = {"message": "Not Found"}
    # sends expected request
    mock_request_get.return_value = MockResponse(message, status_code=404)
    result = runner.invoke(list, ["test"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=fake-token"
    )
    assert result.exit_code == 1
    assert result.exception


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_type_vector(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--type", "vector"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=fake-token&type=vector"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_type_raster(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--type", "raster"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=fake-token&type=raster"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_visibility_public(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--visibility", "public"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=fake-token&visibility=public"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_visibility_private(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--visibility", "private"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=fake-token&visibility=private"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_options(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(
        list, ["test", "--type", "vector", "--visibility", "private"]
    )
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=fake-token&type=vector&visibility=private"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""
