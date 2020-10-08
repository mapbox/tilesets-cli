from click.testing import CliRunner

from mapbox_tilesets.scripts.cli import estimate_area


# rainy day scenarios
def test_cli_estimate_area_features_from_invalid_stdin_geojson():
    message = "Error with feature input. Ensure that feature inputs are valid if they're used and coordinates are formatted correctly. Try 'tilesets --help' for help."
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area, ["--precision", "10m"], input="invalidGeoJson input"
    )
    assert invalidated_result.exit_code == 1
    assert str(invalidated_result.exception) == message


def test_cli_estimate_area_features_from_invalid_geojson_content():
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/invalid-geojson.ldgeojson", "--precision", "1m"],
    )
    assert invalidated_result.exit_code == 1
    # assert the exception type raised is jsondecodeerror?


def test_cli_estimate_area_features_from_nonexistent_geojson_file():
    message = "Error with feature input. Ensure that feature inputs are valid if they're used and coordinates are formatted correctly. Try 'tilesets --help' for help."
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/nonexistent-geojson.ldgeojson", "--precision", "1m"],
    )
    assert str(invalidated_result.exception) == message
    assert invalidated_result.exit_code == 1


def test_cli_estimate_area_no_precision():
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson"],
    )
    assert invalidated_result.exit_code == 2
    assert "Missing option '--precision' / '-p'" in invalidated_result.output


def test_cli_estimate_area_invalid_precision():
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "100m"],
    )
    assert invalidated_result.exit_code == 2
    assert "Invalid value for '--precision' / '-p'" in invalidated_result.output


def test_cli_estimate_area_1cm_precision_without_flag():
    message = "The --force-1cm flag must be present to enable 1cm precision area calculation and may take longer. 1cm precision for tileset processing is only available upon request after contacting Mapbox support."
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "1cm"],
    )
    assert invalidated_result.exit_code == 1
    assert str(invalidated_result.exception) == message


# sunny day scenarios
def test_cli_estimate_area_valid_features_files_and_precision():
    output = '{"km2": 382565, "precision": "10m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "10m"],
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_valid_features_files_and_1cm_precision():
    output = '{"km2": 0, "precision": "1cm", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "1cm", "--force-1cm"],
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output
