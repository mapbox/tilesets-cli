from click.testing import CliRunner

from tilesets.scripts.cli import cli
import os

filepath = os.path.join(os.path.dirname(__file__))


def test_validate_ldgeojson():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["validate-source", filepath + "/fixtures/valid.ldgeojson"]
    )
    assert result.exit_code == 0
    assert "✔ valid" in result.output


def test_validate_invalid_ldgeojson():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["validate-source", filepath + "/fixtures/invalid.ldgeojson"]
    )
    assert result.exit_code == 1
    output = "Error: Invalid JSON on line 1 \n Invalid Content: None \n\n"
    assert output in result.output


def test_validate_invalid_geojson():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["validate-source", filepath + "/fixtures/invalid-geojson.ldgeojson"]
    )
    assert result.exit_code == 1
    output = "Error: Invalid geojson found on line 1 \n Invalid Feature: {'type': 'Feature', 'geometry': {'type': 'Point'}} \n Note - Geojson must be line delimited.\n"
    assert output in result.output
