import json
import pytest

from click.testing import CliRunner
from unittest import mock

from tilesets.scripts.cli import status


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_status(mock_request_get, MockResponse):
    runner = CliRunner()
    # helpers.help_me()
    # sends expected request
    message = {"message": "mock message"}
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(status, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/status?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_status_use_token_flag(mock_request_get, MockResponse):
    runner = CliRunner()
    message = {"message": "mock message"}
    mock_request_get.return_value = MockResponse(message)
    # Provides the flag --token
    result = runner.invoke(status, ["test.id", "--token", "flag-token"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/status?access_token=flag-token"
    )

    assert result.exit_code == 0
    assert json.loads(result.output) == {"message": "mock message"}
