from mapbox_tilesets.scripts.cli import _get_session


def test_get_session():
    s = _get_session("my_application", "1.0.0")
    assert "user-agent" in s.headers
    assert s.headers["user-agent"] == "my_application/1.0.0"
