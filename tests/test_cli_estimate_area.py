from click.testing import CliRunner

from mapbox_tilesets.scripts.cli import estimate_area

# this just keeps running indefinetly
# def test_cli_estimate_area_no_features():
#     runner = CliRunner()
#     invalidated_result = runner.invoke(
#         estimate_area,
#         ["features", " ", "--precision", "10m"],
#     )
#     assert invalidated_result.exit_code == 1


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


# TODO : add output validation
def test_cli_estimate_area_valid_features_files_and_precision():
    runner = CliRunner()
    validated_result = runner.invoke(
        estimate_area,
        ["tests/fixtures/valid.ldgeojson", "-p", "10m"],
    )
    assert validated_result.exit_code == 0
