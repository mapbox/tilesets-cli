import json
import pytest
import click
from click.testing import CliRunner
from unittest import mock

from mapbox_tilesets.scripts.cli import publish


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
def test_cli_publish(mock_request_post):
    runner = CliRunner()
    # sends expected request
    mock_request_post.return_value = MockResponse({"message": "mock message"}, 200)
    result = runner.invoke(publish, ["test.id",  "--accept_pricing"])
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/publish?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 0
    assert (
        "You can view the status of your tileset with the `tilesets status test.id` command."
        in result.output
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.post")
def test_cli_publish_use_token_flag(mock_request_post):
    runner = CliRunner()
    mock_request_post.return_value = MockResponse({"message": "mock message"}, 200)
    # Provides the flag --token
    result = runner.invoke(publish, ["test.id", "--token", "flag-token", "--accept_pricing"])
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/publish?access_token=flag-token"
    )
    assert result.exit_code == 0
    assert (
        "You can view the status of your tileset with the `tilesets status test.id` command."
        in result.output
    )

@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.post")
@mock.patch("click.confirm")
def test_cli_publish_use_token_flag(mock_click_confirm, mock_request_post):
    runner = CliRunner()
    mock_click_confirm.return_value = "y"
    mock_request_post.return_value = MockResponse({"message": "mock message"}, 200)
    # Provides the flag --token
    result = runner.invoke(publish, ["test.id", "--token", "flag-token"])
    mock_click_confirm.assert_called_with(
        "There may be costs associated with uploading and hosting this tileset. Please review the pricing documentation:  https://docs.mapbox.com/accounts/overview/pricing/#tilesets\n To opt out of pricing warnings, pass the --accept_pricing flag. \n Do you want to continue?"
    )
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/publish?access_token=flag-token"
    )
    assert result.exit_code == 0
    assert (
        "You can view the status of your tileset with the `tilesets status test.id` command."
        in result.output
    )
