from click.testing import CliRunner
from unittest import mock

import pytest

from tilesets.scripts.cli import status


class MockResponse:
    def __init__(self, mock_text):
        self.text = mock_text
        self.status_code = 200

    def MockResponse(self):
        return self


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_status(mock_request_get):
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse('{"message":"mock message"}')
    result = runner.invoke(status, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/status?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert '{\n  "message": "mock message"\n}\n' in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_status_use_token_flag(mock_request_get):
    runner = CliRunner()
    mock_request_get.return_value = MockResponse('{"message":"mock message"}')
    # Provides the flag --token
    result = runner.invoke(status, ["test.id", "--token", "flag-token"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/status?access_token=flag-token"
    )
    assert result.exit_code == 0
    assert '{\n  "message": "mock message"\n}\n' in result.output
