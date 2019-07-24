from click.testing import CliRunner
from unittest import mock
import json

# have to set environment variables before importing library
# since they are used in __init__
mock_env=mock.patch.dict('os.environ', {'MAPBOX_ACCESS_TOKEN': 'fake-token', 'MapboxAccessToken': 'test-token'})
mock_env.start()
from tilesets.cli import add_source


class MockResponse():
    def __init__(self, mock_text, status_code):
        self.text = mock_text
        self.status_code = status_code
    def MockResponse(self):
        return self
    def json(self):
        return json.loads(self.text)

@mock.patch('requests.post')
def test_cli_create_source(mock_request_post):
    mock_request_post.return_value = MockResponse('{"id":"mapbox://tileset-source/test-user/hello-world"}', 200)
    runner = CliRunner()
    result = runner.invoke(add_source, ['test-user', 'hello-world', 'tests/fixtures/valid.ldgeojson'])
    assert result.exit_code == 0
    assert 'Validating tests/fixtures/valid.ldgeojson ...\n✔ valid' in result.output
    assert 'Adding tests/fixtures/valid.ldgeojson to mapbox://tileset-source/test-user/hello-world' in result.output
    assert '{\n  "id": "mapbox://tileset-source/test-user/hello-world"\n}\n' in result.output
