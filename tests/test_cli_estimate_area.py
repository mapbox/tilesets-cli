from click.testing import CliRunner

from mapbox_tilesets.scripts.cli import estimate_area


# rainy day scenarios
def test_cli_estimate_area_features_from_invalid_stdin_geojson():
    message = "Error with feature parsing. Ensure that feature inputs are valid and formatted correctly. Try 'tilesets estimate-area --help' for help."
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area, ["--precision", "10m"], input="invalidGeoJson input"
    )
    assert invalidated_result.exit_code == 1
    assert str(invalidated_result.exception) == message


def test_cli_estimate_area_features_from_invalid_geojson_content():
    message = "'properties' is a required property"
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/invalid-geojson.ldgeojson", "--precision", "1m"],
    )
    assert message in str(invalidated_result.exception)
    assert invalidated_result.exit_code == 1


def test_cli_estimate_area_features_from_nonexistent_geojson_file():
    message = "Error with feature parsing. Ensure that feature inputs are valid and formatted correctly. Try 'tilesets estimate-area --help' for help."
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
    message = "The --force-1cm flag must be present to enable 1cm precision area calculation and may take longer for large feature inputs. 1cm precision for tileset processing is only available upon request after contacting Mapbox support."
    runner = CliRunner()
    invalidated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "1cm"],
    )
    assert invalidated_result.exit_code == 1
    assert str(invalidated_result.exception) == message


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


def test_cli_estimate_area_valid_features_files_and_1cm_precision():
    output = '{"km2": "0", "precision": "1cm", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "1cm", "--force-1cm"],
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


# test scenario for each precision and get expected output. The expected km2 are from Mapbox studio and specifying zooms in the recipe
def test_cli_estimate_area_valid_fatures_and_10m_precision():
    output = '{"km2": "1485128", "precision": "10m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area, ["tests/fixtures/precisionTesting.ldgeojson", "-p", "10m"]
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_valid_fatures_and_1m_precision():
    output = '{"km2": "2562", "precision": "1m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area, ["tests/fixtures/precisionTesting.ldgeojson", "-p", "1m"]
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_valid_fatures_and_30cm_precision():
    output = '{"km2": "65", "precision": "30cm", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area, ["tests/fixtures/precisionTesting.ldgeojson", "-p", "30cm"]
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_valid_fatures_and_1cm_precision():
    output = '{"km2": "2", "precision": "1cm", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/precisionTesting.ldgeojson", "-p", "1cm", "--force-1cm"],
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_with_no_validation_flag_and_invalid_feature():
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
