import json
import pytest

from unittest import mock

from click.testing import CliRunner

from mapbox_tilesets.scripts.cli import list_activity

DEFAULT_ENDPOINT = "https://api.mapbox.com/activity/v1/test/tilesets?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&sortby=requests&orderby=desc&limit=100"


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_activity(mock_request_get, MockResponse):
    runner = CliRunner()

    message = [
        {
            "id": "penny.map-one",
            "request_count": 500,
            "last_modified": "2023-06-14T20:18:54.809Z",
        },
        {
            "id": "penny.map-two",
            "request_count": 400,
            "last_modified": "2023-06-14T20:18:54.809Z",
        },
        {
            "id": "penny.map-three",
            "request_count": 300,
            "last_modified": "2023-06-14T20:18:54.809Z",
        },
    ]
    # sends expected request
    mock_request_get.return_value = MockResponse(message)
    MockResponse.headers = {"Link": '<meow.com?start=foo>; rel="next"'}
    result = runner.invoke(list_activity, ["test"])
    mock_request_get.assert_called_with(DEFAULT_ENDPOINT)
    assert json.loads(result.output) == {"data": message, "next": "foo"}
    assert result.exit_code == 0


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_activity_bad_token(mock_request_get, MockResponse):
    runner = CliRunner()

    message = {"message": "Not Found"}
    # sends expected request
    mock_request_get.return_value = MockResponse(message, status_code=404)
    result = runner.invoke(list_activity, ["test"])
    mock_request_get.assert_called_with(DEFAULT_ENDPOINT)
    assert result.exit_code == 1
    assert result.exception


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
def test_cli_list_activity_arguments_valid(mock_request_get, MockResponse):
    runner = CliRunner()
    runner.invoke(
        list_activity,
        [
            "test",
            "--sortby",
            "modified",
            "--orderby",
            "asc",
            "--limit",
            "5",
            "--start",
            "foo",
        ],
    )
    # Arguments are passed into the query string
    mock_request_get.assert_called_with(
        "https://api.mapbox.com/activity/v1/test/tilesets?access_token=pk.eyJ1IjoidGVzdC11c2VyIn0K&sortby=modified&orderby=asc&limit=5&start=foo"
    )


@pytest.mark.usefixtures("token_environ")
@mock.patch("requests.Session.get")
@pytest.mark.parametrize(
    "extra_args",
    [
        (["--sortby", "likes"]),
        (["--orderby", "chaos"]),
        (["--limit", "0"]),
        (["--limit", "501"]),
    ],
)
def test_cli_list_activity_arguments_invalid(
    mock_request_get, MockResponse, extra_args
):
    runner = CliRunner()
    result = runner.invoke(list_activity, ["test"] + extra_args)
    # Invalid argument values should error
    mock_request_get.assert_not_called()
    assert result.exit_code == 2
