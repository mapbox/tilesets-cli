from mapbox_tilesets import __version__


def test_versions():
    mod_version = __version__
    with open("./CHANGELOG.md") as src:
        assert len([line in line for line in src if mod_version in line]) == 1
