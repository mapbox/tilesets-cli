import pytest
import json

from json.decoder import JSONDecodeError


@pytest.fixture(scope="function")
def token_environ(monkeypatch):
    # '{"u":"test-user"}' in base64
    monkeypatch.setenv("MAPBOX_ACCESS_TOKEN", "pk.eyJ1IjoidGVzdC11c2VyIn0K")
    monkeypatch.setenv("MapboxAccessToken", "test-token")


class _MockResponse:
    def __init__(self, mock_json, status_code=200):
        self.text = json.dumps(mock_json)
        self._json = mock_json
        self.status_code = status_code

    def MockResponse(self):
        return self

    def json(self):
        # 201 currently do not have a json response
        if self.status_code == 201:
            raise JSONDecodeError("Expecting value", "", 0)

        return self._json


@pytest.fixture
def MockResponse():
    return _MockResponse


class _MockMultipartEncoding:
    def __init__(self):
        self.content_type = "whatever"
        self.len = 8

    def MockMultipartEncoding(self):
        return self


@pytest.fixture
def MockMultipartEncoding():
    return _MockMultipartEncoding
