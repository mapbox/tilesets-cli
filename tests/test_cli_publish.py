import json
import pytest

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
    mock_request_post.return_value = MockResponse(
        {"message": "mock message", "jobId": "1234fakejob"}, 200
    )
    result = runner.invoke(publish, ["test.id"])
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/publish?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 0
    print(result.output)
    assert (
        '{"message": "mock message", "jobId": "1234fakejob"}\n\n✔ Tileset job received. Visit https://studio.mapbox.com/tilesets/test.id or run tilesets job test.id 1234fakejob to view the status of your tileset.\n'
        in result.output
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.post")
def test_cli_publish_use_token_flag(mock_request_post):
    runner = CliRunner()
    mock_request_post.return_value = MockResponse(
        {"message": "mock message", "jobId": "1234fakejob"}, 200
    )
    # Provides the flag --token
    result = runner.invoke(publish, ["test.id", "--token", "flag-token"])
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/publish?access_token=flag-token"
    )
    assert result.exit_code == 0
    assert (
        '{"message": "mock message", "jobId": "1234fakejob"}\n\n✔ Tileset job received. Visit https://studio.mapbox.com/tilesets/test.id or run tilesets job test.id 1234fakejob to view the status of your tileset.\n'
        in result.output
    )
