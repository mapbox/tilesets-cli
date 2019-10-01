import json
import pytest

from unittest import mock

from click.testing import CliRunner

from tilesets.scripts.cli import list


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
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
@mock.patch("requests.get")
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

    assert [json.loads(l.strip()) for l in result.output.split("\n") if l] == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
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
