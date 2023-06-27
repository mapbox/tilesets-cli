import json
import pytest

from click.testing import CliRunner
from unittest import mock

from mapbox_tilesets.scripts.cli import status
from utils import clean_runner_output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_status(mock_request_get, MockResponse):
    runner = CliRunner()

    # sends expected request
    message = [{"id": "a123", "stage": "processing", "tilesetId": "test.id"}]
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(status, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs?limit=1&access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 0
    expected_status = {
        "id": "test.id",
        "status": "processing",
        "latest_job": "a123",
    }
    assert json.loads(result.output) == expected_status


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_status_use_token_flag(mock_request_get, MockResponse):
    runner = CliRunner()
    message = [{"id": "a123", "stage": "processing", "tilesetId": "test.id"}]
    mock_request_get.return_value = MockResponse(message)
    # Provides the flag --token
    result = runner.invoke(status, ["test.id", "--token", "flag-token"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs?limit=1&access_token=flag-token"
    )

    assert result.exit_code == 0
    expected_status = {
        "id": "test.id",
        "status": "processing",
        "latest_job": "a123",
    }
    assert json.loads(result.output) == expected_status


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_status_error(mock_request_get, MockResponse):
    runner = CliRunner()

    # sends expected request
    message = {"message": "test.id has no jobs."}
    mock_request_get.return_value = MockResponse(message, 404)
    result = runner.invoke(status, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs?limit=1&access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K"
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert clean_runner_output(result.output) == '{"message": "test.id has no jobs."}'
