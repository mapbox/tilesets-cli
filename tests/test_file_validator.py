import os
import pytest

from click.testing import CliRunner

from mapbox_tilesets.scripts.cli import cli

filepath = os.path.join(os.path.dirname(__file__))


def test_validate_ldgeojson():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["validate-source", filepath + "/fixtures/valid.ldgeojson"]
    )
    assert result.exit_code == 0


@pytest.mark.skip("Should this pass w/ cligj?")
def test_validate_invalid_ldgeojson():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["validate-source", filepath + "/fixtures/invalid.ldgeojson"]
    )
    assert result.exit_code == 1


def test_validate_invalid_geojson():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["validate-source", filepath + "/fixtures/invalid-geojson.ldgeojson"]
    )
    assert result.exit_code == 1
