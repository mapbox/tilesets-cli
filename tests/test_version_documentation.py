from mapbox_tilesets import __version__


def test_versions():
    mod_version = __version__
    with open("./CHANGELOG.md") as src:
        assert len([l in l for l in src if mod_version in l]) == 1
