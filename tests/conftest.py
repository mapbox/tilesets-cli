import pytest
import json


@pytest.fixture(scope="function")
def token_environ(monkeypatch):
    monkeypatch.setenv("MAPBOX_ACCESS_TOKEN", "fake-token")
    monkeypatch.setenv("MapboxAccessToken", "test-token")


class _MockResponse:
    def __init__(self, mock_json, status_code=200):
        self.text = json.dumps(mock_json)
        self._json = mock_json
        self.status_code = status_code

    def MockResponse(self):
        return self

    def json(self):
        return self._json


@pytest.fixture
def MockResponse():
    return _MockResponse
