import json
import pytest

from unittest import mock

from click.testing import CliRunner

from mapbox_tilesets.scripts.cli import list


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]
    # sends expected request
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&limit=100"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_verbose(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]
    # sends expected request
    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--verbose"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&limit=100"
    )
    assert result.exit_code == 0

    assert [
        json.loads(tileset.strip()) for tileset in result.output.split("\n") if tileset
    ] == message


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_bad_token(mock_request_get, MockResponse):
    runner = CliRunner()

    message = {"message": "Not Found"}
    # sends expected request
    mock_request_get.return_value = MockResponse(message, status_code=404)
    result = runner.invoke(list, ["test"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&limit=100"
    )
    assert result.exit_code == 1
    assert result.exception


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
@pytest.mark.parametrize("type", ["vector", "raster", "rasterarray"])
def test_cli_list_type(mock_request_get, MockResponse, type):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--type", type])
    mock_request_get.assert_called_with(
        f"https://api.mapbox.com/tilesets/v1/test?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&limit=100&type={type}"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_visibility_public(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--visibility", "public"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&limit=100&visibility=public"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_visibility_private(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--visibility", "private"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&limit=100&visibility=private"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_sortby_created(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--sortby", "created"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&limit=100&sortby=created"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_sortby_modified(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--sortby", "modified"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&limit=100&sortby=modified"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_limit_10(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(list, ["test", "--limit", "10"])
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&limit=10"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_limit_out_of_range(mock_request_get):
    runner = CliRunner()
    result = runner.invoke(list, ["test", "--limit", "0"])
    mock_request_get.assert_not_called()
    assert result.exit_code == 2


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_options(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {"id": "test.tileset-1", "something": "beep"},
        {"id": "test.tileset-2", "something": "boop"},
    ]

    mock_request_get.return_value = MockResponse(message)
    result = runner.invoke(
        list,
        [
            "test",
            "--limit",
            "10",
            "--type",
            "vector",
            "--visibility",
            "private",
            "--sortby",
            "created",
        ],
    )
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/tilesets/v1/test?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&limit=10&type=vector&visibility=private&sortby=created"
    )
    assert result.exit_code == 0
    assert result.output == """test.tileset-1\ntest.tileset-2\n"""
