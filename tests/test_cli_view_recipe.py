from click.testing import CliRunner
from unittest import mock

# have to set environment variables before importing library
# since they are used in __init__
mock_env=mock.patch.dict('os.environ', {'MAPBOX_ACCESS_TOKEN': 'fake-token', 'MapboxAccessToken': 'test-token'})
mock_env.start()
from tilesets.cli import view_recipe


class MockResponse():
    def __init__(self, mock_text):
        self.text = mock_text
        self.status_code = 200
    def MockResponse(self):
        return self


@mock.patch('requests.get')
def test_cli_view_recipe(mock_request_get):
    runner = CliRunner()

    # sends expected request
    mock_request_get.return_value = MockResponse('{"fake":"recipe_data"}')
    result = runner.invoke(view_recipe, ['test.id'])
    mock_request_get.assert_called_with(
        'https://api.mapbox.com/tilesets/v1/test.id/recipe?access_token=fake-token'
    )
    assert result.exit_code == 0
    assert '{\n  "fake": "recipe_data"\n}\n' in result.output


@mock.patch('requests.get')
def test_cli_view_recipe_use_token_flag(mock_request_get):
    runner = CliRunner()
    mock_request_get.return_value = MockResponse('{"fake":"recipe_data"}')
    # Provides the flag --token
    result = runner.invoke(view_recipe, ['test.id', '--token', 'flag-token'])
    mock_request_get.assert_called_with(
        'https://api.mapbox.com/tilesets/v1/test.id/recipe?access_token=flag-token'
    )
    assert result.exit_code == 0
    assert '{\n  "fake": "recipe_data"\n}\n' in result.output


mock_env.stop()
