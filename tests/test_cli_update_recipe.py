from click.testing import CliRunner
from unittest import mock

# have to set environment variables before importing library
# since they are used in __init__
mock_env=mock.patch.dict('os.environ', {'MAPBOX_ACCESS_TOKEN': 'fake-token', 'MapboxAccessToken': 'test-token'})
mock_env.start()
from tilesets.cli import update_recipe


class MockResponse():
    def __init__(self):
        self.status_code = 201
    def MockResponse(self):
        return self


def test_cli_update_recipe_no_recipe():
    runner = CliRunner()
    result = runner.invoke(update_recipe, ['test.id', 'does/not/exist/recipe.json'])
    assert result.exit_code == 2
    assert 'Path "does/not/exist/recipe.json" does not exist' in result.output


@mock.patch('requests.patch')
def test_cli_update_recipe(mock_request_patch):
    runner = CliRunner()

    # sends expected request
    mock_request_patch.return_value = MockResponse()
    result = runner.invoke(update_recipe, ['test.id', 'tests/fixtures/recipe.json'])
    mock_request_patch.assert_called_with(
        'https://api.mapbox.com/tilesets/v1/test.id/recipe?access_token=fake-token',
        json={'minzoom': 0, 'maxzoom': 10, 'layer_name': 'test_layer'}
    )
    assert result.exit_code == 0
    assert 'Updated recipe.' in result.output


@mock.patch('requests.patch')
def test_cli_update_recipe(mock_request_patch):
    runner = CliRunner()
    mock_request_patch.return_value = MockResponse()
    # Provides the flag --token
    result = runner.invoke(update_recipe, ['test.id', 'tests/fixtures/recipe.json', '--token', 'flag-token'])
    mock_request_patch.assert_called_with(
        'https://api.mapbox.com/tilesets/v1/test.id/recipe?access_token=flag-token',
        json={'minzoom': 0, 'maxzoom': 10, 'layer_name': 'test_layer'}
    )
    assert result.exit_code == 0
    assert 'Updated recipe.' in result.output


mock_env.stop()
