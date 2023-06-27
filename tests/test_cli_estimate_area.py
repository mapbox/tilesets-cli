from click.testing import CliRunner

from mapbox_tilesets.scripts.cli import estimate_area
from utils import clean_runner_output


# rainy day scenarios
def test_cli_estimate_area_features_from_invalid_stdin_geojson():
    message = "Error with feature parsing. Ensure that feature inputs are valid and formatted correctly. Try 'tilesets estimate-area --help' for help."
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area, ["--precision", "10m"], input="invalidGeoJson input"
    )
    assert invalidated_result.exit_code == 1
    assert clean_runner_output(invalidated_result.output) == message


def test_cli_estimate_area_features_from_invalid_geojson_content():
    message = "'properties' is a required property"
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/invalid-geojson.ldgeojson", "--precision", "1m"],
    )
    assert message in str(invalidated_result.output)
    assert invalidated_result.exit_code == 1


def test_cli_estimate_area_features_from_nonexistent_geojson_file():
    message = "Error with feature parsing. Ensure that feature inputs are valid and formatted correctly. Try 'tilesets estimate-area --help' for help."
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/nonexistent-geojson.ldgeojson", "--precision", "1m"],
    )
    assert clean_runner_output(invalidated_result.output) == message
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
    message = "The --force-1cm flag must be present to enable 1cm precision area calculation and may take longer for large feature inputs or data with global extents. 1cm precision for tileset processing is only available upon request after contacting Mapbox support."
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "1cm"],
    )
    assert invalidated_result.exit_code == 1
    assert clean_runner_output(invalidated_result.output) == message


def test_cli_estimate_area_invalid_1cm_precision_flag():
    message = "The --force-1cm flag is enabled but the precision is not 1cm."
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "1m", "--force-1cm"],
    )
    assert invalidated_result.exit_code == 1
    assert clean_runner_output(invalidated_result.output) == message


# sunny day scenarios
def test_cli_estimate_area_valid_features_files_and_precision():
    output = '{"km2": "382565", "precision": "10m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "10m"],
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_valid_features_files_and_valid_feature_input():
    output = '{"km2": "382565", "precision": "10m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "10m"],
        input='{"type": "Feature", "geometry": { "type": "Point","coordinates": [125.6, 10.1]},"properties": {"name": "Dinagat Islands"}}',
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_large_valid_features_files_and_valid_feature_input():
    output = '{"km2": "1390828", "precision": "10m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/twostates.ldgeojson", "-p", "10m"],
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_large_valid_features_files_and_valid_feature_input_no_validation():
    output = '{"km2": "1390828", "precision": "10m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/twostates.ldgeojson", "-p", "10m", "--no-validation"],
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_valid_features_files_and_1cm_precision():
    output = '{"km2": "0", "precision": "1cm", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "1cm", "--force-1cm"],
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_with_no_validation_flag_and_invalid_schema():
    output = '{"km2": "382565", "precision": "10m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    # the input is missing "properties"
    validated_result = runner.invoke(
        estimate_area,
        ["--precision", "10m", "--no-validation"],
        input='{"type": "Feature", "geometry": { "type": "Point","coordinates": [125.6, 10.1]}}',
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output
