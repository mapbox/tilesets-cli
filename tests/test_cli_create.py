from unittest import mock
import json

from click.testing import CliRunner
import pytest

from tilesets.cli import create


class MockResponse():
    def __init__(self, mock_text):
        self.text = mock_text
    def MockResponse(self):
        return self


@pytest.mark.usefixtures("token_environ")
def test_cli_create_missing_recipe():
    runner = CliRunner()
    # missing --recipe option
    result = runner.invoke(create, ['test.id'])
    assert result.exit_code == 2
    assert 'Missing option "--recipe"' in result.output


@pytest.mark.usefixtures("token_environ")
def test_cli_create_missing_name():
    runner = CliRunner()
    # missing --name option
    result = runner.invoke(create, ['test.id', '--recipe', 'tests/fixtures/recipe.json'])
    assert result.exit_code == 2
    assert 'Missing option "--name"' in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch('requests.post')
def test_cli_create_success(mock_request_post):
    runner = CliRunner()
    # sends request to proper endpoints
    mock_request_post.return_value = MockResponse('{"message":"mock message"}')
    result = runner.invoke(create, ['test.id', '--recipe', 'tests/fixtures/recipe.json', '--name', 'test name'])
    assert result.exit_code == 0
    mock_request_post.assert_called_with('https://api.mapbox.com/tilesets/v1/test.id?access_token=fake-token', json={'name': 'test name', 'description': '', 'recipe': {'minzoom': 0, 'maxzoom': 10, 'layer_name': 'test_layer'}})
    assert '{\n  "message": "mock message"\n}\n' in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch('requests.post')
def test_cli_create_success_description(mock_request_post):
    runner = CliRunner()
    # sends request with "description" included
    mock_request_post.return_value = MockResponse('{"message":"mock message with description"}')
    result = runner.invoke(create, [
        'test.id',
        '--recipe',
        'tests/fixtures/recipe.json',
        '--name',
        'test name',
        '--description',
        'test description']
    )
    assert result.exit_code == 0
    mock_request_post.assert_called_with('https://api.mapbox.com/tilesets/v1/test.id?access_token=fake-token', json={'name': 'test name', 'description': 'test description', 'recipe': {'minzoom': 0, 'maxzoom': 10, 'layer_name': 'test_layer'}})
    assert '{\n  "message": "mock message with description"\n}\n' in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch('requests.post')
def test_cli_create_private_invalid(mock_request_post):
    runner = CliRunner()
    # sends request with "description" included
    mock_request_post.return_value = MockResponse('{"message":"mock message with description"}')
    result = runner.invoke(create, [
        'test.id',
        '--recipe',
        'tests/fixtures/recipe.json',
        '--name',
        'test name',
        '--privacy',
        'invalid-privacy-value']
    )
    assert result.exit_code == 2
    assert 'Invalid value for "--privacy" / "-p": invalid choice: invalid-privacy-value. (choose from public, private)' in result.output


@pytest.mark.usefixtures("token_environ")
@mock.patch('requests.post')
def test_cli_use_token_flag(mock_request_post):
    runner = CliRunner()
    mock_request_post.return_value = MockResponse('{"message":"mock message"}')
    # Provides the flag --token
    result = runner.invoke(create, ['test.id', '--recipe', 'tests/fixtures/recipe.json', '--name', 'test name', '--token', 'flag-token'])
    assert result.exit_code == 0
    mock_request_post.assert_called_with('https://api.mapbox.com/tilesets/v1/test.id?access_token=flag-token', json={'name': 'test name', 'description': '', 'recipe': {'minzoom': 0, 'maxzoom': 10, 'layer_name': 'test_layer'}})
    assert '{\n  "message": "mock message"\n}\n' in result.output
