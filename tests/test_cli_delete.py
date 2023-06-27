import json
import pytest

from click.testing import CliRunner
from unittest import mock

from mapbox_tilesets.scripts.cli import delete


class MockResponse:
    def __init__(self, mock_json, status_code):
        self.text = json.dumps(mock_json)
        print(self.text)
        self._json = mock_json
        self.status_code = status_code

    def MockResponse(self):
        return self


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.delete")
def test_cli_delete(mock_request_delete):
    runner = CliRunner()

    # sends expected request
    mock_request_delete.return_value = MockResponse("", status_code=200)
    result = runner.invoke(delete, ["test.id"], input="test.id")
    mock_request_delete.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 0
    assert (
        result.output
        == 'To confirm tileset deletion please enter the full tileset id "test.id": test.id\nTileset deleted.\n'
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.delete")
def test_cli_delete_prompt_no(mock_request_delete):
    runner = CliRunner()

    # sends expected request
    mock_request_delete.return_value = MockResponse("", status_code=200)
    result = runner.invoke(delete, ["test.id"], input="wrong.id")
    mock_request_delete.assert_not_called()
    assert result.exit_code == 1
    assert (
        result.output
        == 'To confirm tileset deletion please enter the full tileset id "test.id": wrong.id\nError: wrong.id does not match test.id. Aborted!\n'
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.delete")
def test_cli_delete_force(mock_request_delete):
    runner = CliRunner()

    # sends expected request
    mock_request_delete.return_value = MockResponse("", status_code=204)
    result = runner.invoke(delete, ["test.id", "--force"])
    mock_request_delete.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 0
    assert result.output == "Tileset deleted.\n"


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.delete")
def test_cli_delete_fail(mock_request_delete):
    runner = CliRunner()

    # sends expected request
    mock_request_delete.return_value = MockResponse(
        {"message": "uh oh"}, status_code=422
    )
    result = runner.invoke(delete, ["test.id", "--force"])
    mock_request_delete.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
