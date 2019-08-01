import pytest


@pytest.fixture(scope="function")
def token_environ(monkeypatch):
    monkeypatch.setenv("MAPBOX_ACCESS_TOKEN", "fake-token")
    monkeypatch.setenv("MapboxAccessToken", "test-token")
