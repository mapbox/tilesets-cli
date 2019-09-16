from unittest import mock

from click.testing import CliRunner
import pytest

from tilesets.scripts.cli import jobs, job


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
def test_cli_job(mock_request_get):
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse('{"message":"mock message"}')
    result = runner.invoke(jobs, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert '{\n  "message": "mock message"\n}\n' in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_job_error(mock_request_get):
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponseError(
        '{"message":"mock error message"}'
    )
    result = runner.invoke(jobs, ["test.id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert '{\n  "message": "mock error message"\n}\n' in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_jobs_and_stage(mock_request_get):
    """test jobs + stage endpoint"""
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse('{"message":"mock message"}')
    result = runner.invoke(jobs, ["test.id", "--stage", "complete"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs?stage=complete&access_token=fake-token"
    )
    assert result.exit_code == 0
    assert '{\n  "message": "mock message"\n}\n' in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.get")
def test_cli_single_job(mock_request_get):
    """test job endpoint"""
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse('{"message":"mock message"}')
    result = runner.invoke(job, ["test.id", "job_id"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test.id/jobs/job_id?access_token=fake-token"
    )
    assert result.exit_code == 0
    assert '{\n  "message": "mock message"\n}\n' in result.output
