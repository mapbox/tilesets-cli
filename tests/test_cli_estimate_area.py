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


def test_cli_estimate_area_valid_features_files_and_valid_feature_input():
    output = '{"km2": 382565, "precision": "10m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "10m"],
        input='{"type": "Feature", "geometry": { "type": "Point","coordinates": [125.6, 10.1]},"properties": {"name": "Dinagat Islands"}}',
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


# TODO: need a good geojson file to have 1cm km2 area + need a way to verify each area is correct
# test scenario for each precision and get expected output. The expected km2 are from uploading the tileset onto Mapbox studio.
def test_cli_estimate_area_valid_fatures_and_10m_precision():
    output = '{"km2": 741915, "precision": "10m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area, ["tests/fixtures/precisionTesting.ldgeojson", "-p", "10m"]
    )
    assert validated_result.exit_code == 0
    assert validated_result.output == output


def test_cli_estimate_area_valid_fatures_and_1m_precision():
    # output = '{"km2": "2092", "precision": "1m", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area, ["tests/fixtures/precisionTesting.ldgeojson", "-p", "1m"]
    )
    # print(validated_result.output)
    assert validated_result.exit_code == 0
    # assert validated_result.output == output


def test_cli_estimate_area_valid_fatures_and_30cm_precision():
    # output = '{"km2": "29", "precision": "30cm", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area, ["tests/fixtures/precisionTesting.ldgeojson", "-p", "30cm"]
    )
    # print(validated_result.output)
    assert validated_result.exit_code == 0
    # assert validated_result.output == output


def test_cli_estimate_area_valid_fatures_and_1cm_precision():
    # output = '{"km2": "0", "precision": "1cm", "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets"}\n'
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/precisionTesting.ldgeojson", "-p", "1cm", "--force-1cm"],
    )
    # print(validated_result.output)
    assert validated_result.exit_code == 0
    # assert validated_result.output == output


# TODO : What would be not needed to be validated and still work w/ area calculation???
# no-validation flag
# def test_cli_estimate_area_with_no_validation_flag_and_invalid_feature():
#     runner = CliRunner()
#     validated_result = runner.invoke(
#         estimate_area, ["--precision", "10m"], input='{"type": "Feature", "geometry": { "type": "Point"}}'
#     )
#     print(validated_result.output)
#     assert validated_result.exit_code == 0
