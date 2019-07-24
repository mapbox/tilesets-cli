from click.testing import CliRunner
from unittest import mock
import json

# have to set environment variables before importing library
# since they are used in __init__
mock_env=mock.patch.dict('os.environ', {'MAPBOX_ACCESS_TOKEN': 'fake-token', 'MapboxAccessToken': 'test-token'})
mock_env.start()
from tilesets.cli import upload


class MockResponse():
    def __init__(self, mock_text, status_code):
        self.text = mock_text
        self.status_code = status_code
    def MockResponse(self):
        return self
    def json(self):
        return json.loads(self.text)


def test_cli_create_missing_files():
    runner = CliRunner()
    # missing files argument
    result = runner.invoke(upload, ['test.id'])
    assert result.exit_code == 2
    assert 'Missing argument "FILES...' in result.output


def test_cli_upload_invalid_filepath():
    runner = CliRunner()
    # file path does not exist
    result = runner.invoke(upload, ['test.id', 'does/not/exist.jpg'])
    assert result.exit_code == 2
    assert 'Path "does/not/exist.jpg" does not exist.' in result.output


@mock.patch('requests.post')
@mock.patch('tilesets.scripts.uploader.upload')
def test_cli_success_single_file_with_validation(mock_uploader, mock_request_post):
    runner = CliRunner()
    mock_request_post.return_value = MockResponse('{"credentialToken":"1234"}', 200)
    result = runner.invoke(upload, ['test.id', 'tests/fixtures/valid.ldgeojson'])

    mock_request_post.assert_called_with('https://api.mapbox.com/tilesets/v1/test.id/credentials?access_token=fake-token')
    mock_uploader.assert_called_with('tests/fixtures/valid.ldgeojson', {'credentialToken': '1234'})
    assert result.exit_code == 0
    assert 'Done staging files. You can publish these to a tileset with `tilesets publish test.id`' in result.output


def test_cli_failure_single_invalid_file_with_validation():
    runner = CliRunner()
    result = runner.invoke(upload, ['test.id', 'tests/fixtures/invalid.ldgeojson'])

    assert result.exit_code == 1
    assert 'Error: Invalid JSON on line 1' in result.output

@mock.patch('requests.post')
@mock.patch('tilesets.scripts.uploader.upload')
def test_cli_success_single_invalid_file_without_validation(mock_uploader, mock_request_post):
    runner = CliRunner()
    mock_request_post.return_value = MockResponse('{"credentialToken":"1234"}', 200)
    result = runner.invoke(upload, ['test.id', 'tests/fixtures/invalid.ldgeojson', '--no-validation'])

    mock_request_post.assert_called_with('https://api.mapbox.com/tilesets/v1/test.id/credentials?access_token=fake-token')
    mock_uploader.assert_called_with('tests/fixtures/invalid.ldgeojson', {'credentialToken': '1234'})
    assert result.exit_code == 0

@mock.patch('requests.post')
@mock.patch('tilesets.scripts.utils.print_response')
def test_cli_failure_500_error(mock_print, mock_request_post):
    runner = CliRunner()
    mock_request_post.return_value = MockResponse('{"error":"my error"}', 500)
    result = runner.invoke(upload, ['test.id', 'tests/fixtures/invalid.ldgeojson', '--no-validation'])

    mock_request_post.assert_called_with('https://api.mapbox.com/tilesets/v1/test.id/credentials?access_token=fake-token')
    mock_print.assert_called_with('{"error":"my error"}')
    assert result.exit_code == 0

@mock.patch('requests.post')
def test_cli_failure_500_no_json(mock_request_post):
    runner = CliRunner()
    mock_request_post.return_value = MockResponse('this is an non JSON api error', 500)
    result = runner.invoke(upload, ['test.id', 'tests/fixtures/invalid.ldgeojson', '--no-validation'])
    mock_request_post.assert_called_with('https://api.mapbox.com/tilesets/v1/test.id/credentials?access_token=fake-token')
    assert 'Failure \nthis is an non JSON api error\n' in result.output
    assert result.exit_code == 0

@mock.patch('requests.post')
@mock.patch('tilesets.scripts.uploader.upload')
def test_cli_upload_use_token_flag(mock_uploader, mock_request_post):
    runner = CliRunner()
    mock_request_post.return_value = MockResponse('{"credentialToken":"1234"}', 200)
    # Provides the flag --token
    result = runner.invoke(upload, ['test.id', 'tests/fixtures/valid.ldgeojson', '--token', 'flag-token'])

    mock_request_post.assert_called_with('https://api.mapbox.com/tilesets/v1/test.id/credentials?access_token=flag-token')
    mock_uploader.assert_called_with('tests/fixtures/valid.ldgeojson', {'credentialToken': '1234'})
    assert result.exit_code == 0
    assert 'Done staging files. You can publish these to a tileset with `tilesets publish test.id`' in result.output


mock_env.stop()
