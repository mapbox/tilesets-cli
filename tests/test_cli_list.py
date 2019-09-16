from unittest import mock

from click.testing import CliRunner
import pytest

from tilesets.scripts.cli import list


class MockResponse:
    def __init__(self, mock_text):
        self.text = mock_text
        self.status_code = 200

    def MockResponse(self):
        return self


class MockResponseError:
    def __init__(self, mock_text):
        self.text = mock_text
        self.status_code = 404

    def MockResponse(self):
        return self


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_list(mock_request_get):
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse(
        '[{"id":"test.tileset-1","something":"beep"},{"id":"test.tileset-2","something":"boop"}]'
    )
    result = runner.invoke(list, ["test"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert "test.tileset-1\ntest.tileset-2\n" in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_list_verbose(mock_request_get):
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse(
        '[{"id":"test.tileset-1","something":"beep"},{"id":"test.tileset-2","something":"boop"}]'
    )
    result = runner.invoke(list, ["test", "--verbose"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert '"something": "beep"\n' in result.output
    assert '"something": "boop"\n' in result.output
