import json
import pytest
from unittest import mock

from click.testing import CliRunner

from mapbox_tilesets.scripts.cli import estimate_cu


@pytest.mark.usefixtures("token_environ")
@pytest.mark.usefixtures("api_environ")
@mock.patch("requests.Session.get")
def test_cli_estimate_cu_tileset_no_sources(mock_request_get, MockResponse):
    runner = CliRunner()

    tileset_id = "my.tileset"
    msg = {"message": "mock message"}

    mock_request_get.return_value = MockResponse(msg)
    result = runner.invoke(estimate_cu, [tileset_id])
    mock_request_get.assert_called_with(
        f"https://api.mapbox.com/tilesets/v1/{tileset_id}/estimate",
        params={
            "filesize": 0,
            "band_count": 15,
            "access_token": "pk.eyJ1IjoidGVzdC11c2VyIn0K",
        },
    )

    assert result.exit_code == 1
    assert (
        result.output
        == f"[warning] estimating '{tileset_id}' with a default global bounds\nError: {json.dumps(msg)}\n"
    )


@pytest.mark.usefixtures("token_environ")
@pytest.mark.usefixtures("api_environ")
@mock.patch("requests.Session.get")
@mock.patch("glob.glob")
def test_cli_estimate_cu_tileset_with_sources_raw(
    mock_glob, mock_request_get, MockResponse
):
    runner = CliRunner()

    tileset_id = "my.tileset"
    msg = {"cu": "5"}

    mock_request_get.return_value = MockResponse(msg)
    mock_glob.return_value = ["myfile.grib2"]
    result = runner.invoke(
        estimate_cu, [tileset_id, "-s", "/my/sources/*.grib2", "--raw"]
    )
    mock_request_get.assert_called_with(
        f"https://api.mapbox.com/tilesets/v1/{tileset_id}/estimate",
        params={
            "filesize": 0,
            "band_count": 15,
            "access_token": "pk.eyJ1IjoidGVzdC11c2VyIn0K",
        },
    )

    assert result.exit_code == 0
    assert json.loads(result.output) == msg


@pytest.mark.usefixtures("token_environ")
@pytest.mark.usefixtures("api_environ")
@mock.patch("requests.Session.get")
@mock.patch("glob.glob")
def test_cli_estimate_cu_tileset_with_sources(
    mock_glob, mock_request_get, MockResponse
):
    runner = CliRunner()

    tileset_id = "my.tileset"
    msg = {"cu": "5"}

    mock_request_get.return_value = MockResponse(msg)
    mock_glob.return_value = ["myfile.grib2"]
    result = runner.invoke(estimate_cu, [tileset_id, "-s", "/my/sources/*.grib2"])
    mock_request_get.assert_called_with(
        f"https://api.mapbox.com/tilesets/v1/{tileset_id}/estimate",
        params={
            "filesize": 0,
            "band_count": 15,
            "access_token": "pk.eyJ1IjoidGVzdC11c2VyIn0K",
        },
    )

    assert result.exit_code == 0
    assert (
        result.output
        == f"\nEstimated CUs for '{tileset_id}': {msg['cu']}. To publish your tileset, run 'tilesets publish'.\n"
    )


@pytest.mark.usefixtures("token_environ")
@pytest.mark.usefixtures("api_environ")
@mock.patch("requests.Session.get")
@mock.patch("glob.glob")
def test_cli_estimate_cu_tileset_with_zoom_overrides(
    mock_glob, mock_request_get, MockResponse
):
    runner = CliRunner()

    tileset_id = "my.tileset"
    msg = {"cu": "5"}

    mock_request_get.return_value = MockResponse(msg)
    mock_glob.return_value = ["myfile.grib2"]
    result = runner.invoke(
        estimate_cu,
        [tileset_id, "-s", "/my/sources/*.grib2", "--minzoom", 1, "--maxzoom", 6],
    )
    mock_request_get.assert_called_with(
        f"https://api.mapbox.com/tilesets/v1/{tileset_id}/estimate",
        params={
            "minzoom": 1,
            "maxzoom": 6,
            "filesize": 0,
            "band_count": 15,
            "access_token": "pk.eyJ1IjoidGVzdC11c2VyIn0K",
        },
    )

    assert result.exit_code == 0
    assert (
        result.output
        == f"\nEstimated CUs for '{tileset_id}': {msg['cu']}. To publish your tileset, run 'tilesets publish'.\n"
    )


@pytest.mark.usefixtures("token_environ")
@pytest.mark.usefixtures("api_environ")
@mock.patch("requests.Session.get")
@mock.patch("glob.glob")
def test_cli_estimate_cu_tileset_with_bands_override(
    mock_glob, mock_request_get, MockResponse
):
    runner = CliRunner()

    tileset_id = "my.tileset"
    msg = {"cu": "5"}

    mock_request_get.return_value = MockResponse(msg)
    mock_glob.return_value = ["myfile.grib2"]
    result = runner.invoke(
        estimate_cu,
        [
            tileset_id,
            "-s",
            "/my/sources/*.grib2",
            "-b",
            10,
            "--minzoom",
            1,
            "--maxzoom",
            6,
        ],
    )
    mock_request_get.assert_called_with(
        f"https://api.mapbox.com/tilesets/v1/{tileset_id}/estimate",
        params={
            "minzoom": 1,
            "maxzoom": 6,
            "filesize": 0,
            "band_count": 10,
            "access_token": "pk.eyJ1IjoidGVzdC11c2VyIn0K",
        },
    )

    assert result.exit_code == 0
    assert (
        result.output
        == f"\nEstimated CUs for '{tileset_id}': {msg['cu']}. To publish your tileset, run 'tilesets publish'.\n"
    )
