"""Source-related CLI commands."""

import base64
import builtins
import json

import click
import cligj
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from mapbox_tilesets import errors, utils
from mapbox_tilesets.scripts.cli_common import (
    _upload_file,
    validate_source_id,
    validate_stream,
)


@click.command("validate-source")
@cligj.features_in_arg
def validate_source(features):
    """Validate your source file.
    $ tilesets validate-source <path/to/your/src/file>
    """
    click.echo("Validating features", err=True)

    for index, feature in enumerate(features):
        utils.validate_geojson(index, feature)

    click.echo("✔ valid")


@click.command("upload-source")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, callback=validate_source_id, type=str)
@cligj.features_in_arg
@click.option("--no-validation", is_flag=True, help="Bypass source file validation")
@click.option("--quiet", is_flag=True, help="Don't show progress bar")
@click.option(
    "--replace",
    is_flag=True,
    help="Replace the existing source with the new source file",
)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
@click.pass_context
def upload_source(
    ctx, username, id, features, no_validation, quiet, replace, token=None, indent=None
):
    """Create a new tileset source, or add data to an existing tileset source.
    Optionally, replace an existing tileset source.

    tilesets upload-source <username> <source_id> <path/to/source/data>
    """
    return _upload_file(
        ctx, username, id, features, no_validation, quiet, replace, False, token, indent
    )


@click.command("upload-raster-source")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, callback=validate_source_id, type=str)
@click.argument("inputs", nargs=-1, required=True, type=click.File("r"))
@click.option("--quiet", is_flag=True, help="Don't show progress bar")
@click.option(
    "--replace",
    is_flag=True,
    help="Replace the existing source with raster source file ",
)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
@click.pass_context
def upload_raster_source(
    ctx, username, id, inputs, quiet, replace, token=None, indent=None
):
    """Create a new raster tileset source, or add data to an existing tileset source.
    Optionally, replace an existing tileset source.

    tilesets upload-source <username> <source_id> <path/to/source/data>
    """
    return _upload_raster_source(
        ctx, username, id, inputs, quiet, replace, token, indent
    )


def _upload_raster_source(
    ctx, username, id, inputs, quiet, replace, token=None, indent=None
):
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = (
        f"{mapbox_api}/tilesets/v1/sources/{username}/{id}?access_token={mapbox_token}"
    )

    method = "post"
    if replace:
        method = "put"

    # This does the decoding by hand instead of using pyjwt because
    # pyjwt rejects tokens that don't pad the base64 with = signs.
    token_parts = mapbox_token.split(".")
    if len(token_parts) < 2:
        raise errors.TilesetsError(
            f"Token {mapbox_token} does not contain a payload component"
        )
    else:
        while len(token_parts[1]) % 4 != 0:
            token_parts[1] = token_parts[1] + "="
        body = json.loads(base64.b64decode(token_parts[1]))
        if "u" in body:
            if username != body["u"]:
                raise errors.TilesetsError(
                    f"Token username {body['u']} does not match username {username}"
                )
        else:
            raise errors.TilesetsError(
                f"Token {mapbox_token} does not contain a username"
            )

    if len(inputs) > 10:
        raise errors.TilesetsError("Maximum 10 files can be uploaded at once.")

    for item in inputs:
        m = MultipartEncoder(
            fields={"file": ("file", open(item.name, "rb"), "multipart/form-data")}
        )
        if quiet:
            resp = getattr(s, method)(
                url,
                data=m,
                headers={
                    "Content-Disposition": "multipart/form-data",
                    "Content-type": m.content_type,
                },
            )
        else:
            prog = click.progressbar(
                length=m.len, fill_char="=", width=0, label="upload progress"
            )
            with prog:

                def callback(m):
                    prog.pos = m.bytes_read
                    prog.update(0)  # Step is 0 because we set pos above

                monitor = MultipartEncoderMonitor(m, callback)
                resp = getattr(s, method)(
                    url,
                    data=monitor,
                    headers={
                        "Content-Disposition": "multipart/form-data",
                        "Content-type": monitor.content_type,
                    },
                )

    if resp.status_code == 200:
        click.echo(json.dumps(resp.json(), indent=indent))
    else:
        raise errors.TilesetsError(resp.text)


@click.command("add-source", hidden=True)
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
@cligj.features_in_arg
@click.option("--no-validation", is_flag=True, help="Bypass source file validation")
@click.option("--quiet", is_flag=True, help="Don't show progress bar")
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
@click.pass_context
def add_source(
    ctx, username, id, features, no_validation, quiet, token=None, indent=None
):
    """[DEPRECATED] Create/add/replace a tileset source. Use upload-source instead.

    tilesets add-source <username> <source_id> <path/to/source/data>
    """
    return _upload_file(
        ctx, username, id, features, no_validation, quiet, False, False, token, indent
    )


@click.command("view-source")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def view_source(username, id, token=None, indent=None):
    """View a Tileset Source's information

    tilesets view-source <username> <source_id>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/sources/{1}/{2}?access_token={3}".format(
        mapbox_api, username, id, mapbox_token
    )
    r = s.get(url)
    if r.status_code == 200:
        click.echo(json.dumps(r.json(), indent=indent))
    else:
        raise errors.TilesetsError(r.text)


@click.command("delete-source")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
@click.option("--force", "-f", is_flag=True, help="Circumvents confirmation prompt")
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def delete_source(username, id, force, token=None):
    """Delete a Tileset Source + all of its files.

    tilesets delete-source <username> <source_id>
    """
    if not force:
        val = click.prompt(
            'To confirm source deletion please enter the full source id "{0}/{1}"'.format(
                username, id
            ),
            type=str,
        )
        if val != f"{username}/{id}":
            raise click.ClickException(
                f"{val} does not match {username}/{id}. Aborted!"
            )

    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/sources/{1}/{2}?access_token={3}".format(
        mapbox_api, username, id, mapbox_token
    )
    r = s.delete(url)
    if r.status_code == 204:
        click.echo("Source deleted.")
    else:
        raise errors.TilesetsError(r.text)


@click.command("list-sources")
@click.argument("username", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def list_sources(username, token=None):
    """List all Tileset Sources for an account. Response is an un-ordered array of sources.

    tilesets list-sources <username>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/sources/{1}?access_token={2}".format(
        mapbox_api, username, mapbox_token
    )
    r = s.get(url)
    if r.status_code == 200:
        for source in r.json():
            click.echo(source["id"])
    else:
        raise errors.TilesetsError(r.text)


@click.command("estimate-area")
@cligj.features_in_arg
@click.option(
    "--precision",
    "-p",
    required=True,
    type=click.Choice(["10m", "1m", "30cm", "1cm"]),
    help="Precision level",
)
@click.option(
    "--no-validation",
    required=False,
    is_flag=True,
    help="Bypass source file validation",
)
@click.option(
    "--force-1cm",
    required=False,
    is_flag=True,
    help="Enables 1cm precision",
)
def estimate_area(features, precision, no_validation=False, force_1cm=False):
    """Estimate area of features with a precision level. Requires extra installation steps: see https://github.com/mapbox/tilesets-cli/blob/master/README.md

    tilesets estimate-area <features> <precision>

    features must be a list of paths to local files containing GeoJSON feature collections or feature sequences from argument or stdin, or a list of string-encoded coordinate pairs of the form "[lng, lat]", or "lng, lat", or "lng lat".
    """
    filter_features = utils.load_module("supermercado.super_utils").filter_features

    area = 0
    if precision == "1cm" and not force_1cm:
        raise errors.TilesetsError(
            "The --force-1cm flag must be present to enable 1cm precision area calculation and may take longer for large feature inputs or data with global extents. 1cm precision for tileset processing is only available upon request after contacting Mapbox support."
        )
    if precision != "1cm" and force_1cm:
        raise errors.TilesetsError(
            "The --force-1cm flag is enabled but the precision is not 1cm."
        )

    try:
        # expect users to bypass source validation when users rerun command and their features passed validation previously
        if not no_validation:
            features = validate_stream(features)
        # builtins.list because there is a list command in the cli & will thrown an error
        # It is a list at all because calculate_tiles_area does not work with a stream
        features = builtins.list(filter_features(features))
    except (ValueError, json.decoder.JSONDecodeError):
        raise errors.TilesetsError(
            "Error with feature parsing. Ensure that feature inputs are valid and formatted correctly. Try 'tilesets estimate-area --help' for help."
        )

    area = utils.calculate_tiles_area(features, precision)
    area = str(int(round(area)))

    click.echo(
        json.dumps(
            {
                "km2": area,
                "precision": precision,
                "pricing_docs": "For more information, visit https://www.mapbox.com/pricing/#tilesets",
            }
        )
    )
