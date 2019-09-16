from click.testing import CliRunner
from unittest import mock

import pytest

from tilesets.scripts.cli import publish


class MockResponse:
    def __init__(self, mock_text, status_code):
        self.text = mock_text
        self.status_code = status_code

    def MockResponse(self):
        return self


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.post")
def test_cli_publish(mock_request_post):
    runner = CliRunner()

    # sends expected request
    mock_request_post.return_value = MockResponse('{"message":"mock message"}', 200)
    result = runner.invoke(publish, ["test.id"])
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/publish?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert (
        "You can view the status of your tileset with the `tilesets status test.id` command."
        in result.output
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.post")
def test_cli_publish_use_token_flag(mock_request_post):
    runner = CliRunner()
    mock_request_post.return_value = MockResponse('{"message":"mock message"}', 200)
    # Provides the flag --token
    result = runner.invoke(publish, ["test.id", "--token", "flag-token"])
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/publish?access_token=flag-token"
    )
    assert result.exit_code == 0
    assert (
        "You can view the status of your tileset with the `tilesets status test.id` command."
        in result.output
    )
