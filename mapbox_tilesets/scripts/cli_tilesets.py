"""Tileset-related CLI commands."""

import json

import click

from mapbox_tilesets import errors, utils


@click.command("status")
@click.argument("tileset", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def status(tileset, token=None, indent=None):
    """View the current queue/processing/complete status of your tileset.

    tilesets status <tileset_id>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/{1}/jobs?limit=1&access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    r = s.get(url)

    if r.status_code != 200:
        raise errors.TilesetsError(r.text)

    status = {}
    for job in r.json():
        status["id"] = job["tilesetId"]
        status["latest_job"] = job["id"]
        status["status"] = job["stage"]

    click.echo(json.dumps(status, indent=indent))


@click.command("tilejson")
@click.argument("tileset", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
@click.option(
    "--secure", required=False, is_flag=True, help="receive HTTPS resource URLs"
)
def tilejson(tileset, token=None, indent=None, secure=False):
    """View the TileJSON of a particular tileset.
    Can take a comma-separated list of tilesets for a composited TileJSON.

    tilesets tilejson <tileset_id>,<tileset_id>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()

    # validate tilesets by splitting comma-delimted string
    # and rejoining it
    for t in tileset.split(","):
        if not utils.validate_tileset_id(t):
            raise errors.TilesetNameError(t)

    url = "{0}/v4/{1}.json?access_token={2}".format(mapbox_api, tileset, mapbox_token)
    if secure:
        url = url + "&secure"

    r = s.get(url)
    if r.status_code == 200:
        click.echo(json.dumps(r.json(), indent=indent))
    else:
        raise errors.TilesetsError(r.text)


@click.command("list")
@click.argument("username", required=True, type=str)
@click.option(
    "--verbose",
    "-v",
    required=False,
    is_flag=True,
    help="Will print all tileset information",
)
@click.option(
    "--type",
    required=False,
    type=click.Choice(["vector", "raster", "rasterarray"]),
    help="Filter results by tileset type",
)
@click.option(
    "--visibility",
    required=False,
    type=click.Choice(["public", "private"]),
    help="Filter results by visibility",
)
@click.option(
    "--sortby",
    required=False,
    type=click.Choice(["created", "modified"]),
    help="Sort the results by their created or modified timestamps",
)
@click.option(
    "--limit",
    required=False,
    type=click.IntRange(1, 500),
    default=100,
    help="The maximum number of results to return, from 1 to 500 (default 100)",
)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def list(
    username,
    verbose,
    type=None,
    visibility=None,
    sortby=None,
    limit=None,
    token=None,
    indent=None,
):
    """List all tilesets for an account.
    By default the response is a simple list of tileset IDs.
    If you would like an array of all tileset's information,
    use the --versbose flag.

    tilesets list <username>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/{1}?access_token={2}".format(
        mapbox_api, username, mapbox_token
    )
    url = "{0}&limit={1}".format(url, limit) if limit else url
    url = "{0}&type={1}".format(url, type) if type else url
    url = "{0}&visibility={1}".format(url, visibility) if visibility else url
    url = "{0}&sortby={1}".format(url, sortby) if sortby else url
    r = s.get(url)
    if r.status_code == 200:
        if verbose:
            for tileset in r.json():
                click.echo(json.dumps(tileset, indent=indent))
        else:
            for tileset in r.json():
                click.echo(tileset["id"])
    else:
        raise errors.TilesetsError(r.text)
