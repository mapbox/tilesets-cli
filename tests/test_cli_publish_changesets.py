import json
import pytest

from click.testing import CliRunner
from unittest import mock

from mapbox_tilesets.scripts.cli import publish_changesets

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
def test_cli_publish_changesets(mock_request_post):
    runner = CliRunner()

    # sends expected request
    mock_request_post.return_value = MockResponse(
        {"message": "mock message", "jobId": "1234fakejob"}, 200
    )
    result = runner.invoke(publish_changesets, ["test.id", "tests/fixtures/changeset-payload.json"])
    mock_request_post.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/publish-changesets?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K",
        json={
            "layers": {
                "trees": {
                    "changeset": "mapbox://tileset-changeset/test.id/test-changeset-id"
                }
            }
        },
    )
    assert result.exit_code == 0
    print(result.output)
    assert (
        '{"message": "mock message", "jobId": "1234fakejob"}'
        in result.output
    )