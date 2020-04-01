import json
import pytest

from unittest import mock
from click.testing import CliRunner

from mapbox_tilesets.scripts.cli import jobs, job


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_job(mock_request_get, MockResponse):
    runner = CliRunner()

    # sends expected request
    message = {"message": "mock message"}
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(jobs, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == message


# noting for future that this test really is a copy of above
@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_job_error(mock_request_get, MockResponse):
    runner = CliRunner()

    # sends expected request
    message = {"message": "mock error message"}
    mock_request_get.return_value = MockResponse(message, status_code=404)
    result = runner.invoke(jobs, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_jobs_and_stage(mock_request_get, MockResponse):
    """test jobs + stage endpoint"""
    runner = CliRunner()

    # sends expected request
    message = {"message": "mock message"}
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(jobs, ["test.id", "--stage", "complete"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs?stage=complete&access_token=fake-token"
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_single_job(mock_request_get, MockResponse):
    """test job endpoint"""
    runner = CliRunner()

    # sends expected request
    message = {"message": "mock message"}
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(job, ["test.id", "job_id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs/job_id?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == message
