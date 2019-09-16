from tilesets.utils import format_response, validate_tileset_id


def test_format_response_json():
    response = '{"bada": "bing"}'

    assert format_response(response) == response


def test_format_response_indent_json():
    response = '{"bada": "bing"}'

    assert format_response(response, indent=2) == """{\n  \"bada\": \"bing\"\n}"""


def test_format_response_indent_backwards_json():
    response = """{\n  \"bada\": \"bing\"\n}"""

    assert format_response(response) == '{"bada": "bing"}'


def test_format_response_string():
    response = "hi"

    assert format_response(response) == response


def test_validate_tileset_id():
    tileset = "iama.test"

    assert validate_tileset_id(tileset)


def test_validate_tileset_id_badfmt():
    tileset = "iama.test.ok"

    assert not validate_tileset_id(tileset)


def test_validate_tileset_id_toolong():
    tileset = "hellooooooooooooooooooooooooooooooo.hiiiiiiiuuuuuuuuuuuuuuuuuuuuuu"

    assert not validate_tileset_id(tileset)
