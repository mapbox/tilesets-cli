import json
import pytest

from click.testing import CliRunner
from unittest import mock

from mapbox_tilesets.scripts.cli import delete


class MockResponse:
    def __init__(self, mock_json, status_code):
        self.text = json.dumps(mock_json)
        self._json = mock_json
        self.status_code = status_code

    def MockResponse(self):
        return self


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.delete")
def test_cli_delete(mock_request_delete):
    runner = CliRunner()

    # sends expected request
    mock_request_delete.return_value = MockResponse("", status_code=204)
    result = runner.invoke(delete, ["test.id"], input="y")
    mock_request_delete.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert result.output == "Are you sure you want to delete test.id? [y/N]: y\n"


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.delete")
def test_cli_delete_force(mock_request_delete):
    runner = CliRunner()

    # sends expected request
    mock_request_delete.return_value = MockResponse("", status_code=204)
    result = runner.invoke(delete, ["test.id", "--force"])
    mock_request_delete.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert result.output == ""
