from mapbox_tilesets.utils import validate_tileset_id


def test_validate_tileset_id():
    tileset = "iama.test"

    assert validate_tileset_id(tileset)


def test_validate_tileset_id_badfmt():
    tileset = "iama.test.ok"

    assert not validate_tileset_id(tileset)


def test_validate_tileset_id_toolong():
    tileset = "hellooooooooooooooooooooooooooooooo.hiiiiiiiuuuuuuuuuuuuuuuuuuuuuu"

    assert not validate_tileset_id(tileset)
