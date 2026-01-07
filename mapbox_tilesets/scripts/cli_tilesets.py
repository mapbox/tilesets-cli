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


@click.command("create")
@click.argument("tileset", required=True, type=str)
@click.option(
    "--recipe",
    "-r",
    required=True,
    type=click.Path(exists=True),
    help="path to a Recipe JSON document",
)
@click.option("--name", "-n", required=True, type=str, help="name of the tileset")
@click.option(
    "--description", "-d", required=False, type=str, help="description of the tileset"
)
@click.option(
    "--privacy",
    "-p",
    required=False,
    type=click.Choice(["public", "private"]),
    help="set the tileset privacy options",
)
@click.option(
    "--attribution",
    required=False,
    type=str,
    help="attribution for the tileset in the form of a JSON string - Array<Object<text,link>>",
)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def create(
    tileset,
    recipe,
    name=None,
    description=None,
    privacy=None,
    attribution=None,
    token=None,
    indent=None,
):
    """Create a new tileset with a recipe.

    $ tilesets create <tileset_id>

    <tileset_id> is in the form of username.handle - for example "mapbox.neat-tileset".
    The handle may only include "-" or "_" special characters and must be 32 characters or fewer.
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/{1}?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    body = {}
    body["name"] = name or ""
    body["description"] = description or ""
    if privacy:
        body["private"] = True if privacy == "private" else False

    if not utils.validate_tileset_id(tileset):
        raise errors.TilesetNameError(tileset)

    if recipe:
        with open(recipe) as json_recipe:
            body["recipe"] = json.load(json_recipe)

    if attribution:
        try:
            body["attribution"] = json.loads(attribution)
        except:
            click.echo("Unable to parse attribution JSON")
            click.exit(1)

    r = s.post(url, json=body)

    click.echo(json.dumps(r.json(), indent=indent))


@click.command("publish")
@click.argument("tileset", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def publish(tileset, token=None, indent=None):
    """Publish your tileset.

    Only supports tilesets created with the Mapbox Tiling Service.

    tilesets publish <tileset_id>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/{1}/publish?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    r = s.post(url)
    if r.status_code == 200:
        response_msg = r.json()
        click.echo(json.dumps(response_msg, indent=indent))

        studio_url = click.style(
            f"https://studio.mapbox.com/tilesets/{tileset}", bold=True
        )
        job_id = response_msg["jobId"]
        job_cmd = click.style(f"tilesets job {tileset} {job_id}", bold=True)
        message = f"\n✔ Tileset job received. Visit {studio_url} or run {job_cmd} to view the status of your tileset."
        click.echo(
            message,
            err=True,  # print to stderr so the JSON output can be parsed separately from the success message
        )
    else:
        raise errors.TilesetsError(r.text)


@click.command("update")
@click.argument("tileset", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
@click.option("--name", "-n", required=False, type=str, help="name of the tileset")
@click.option(
    "--description", "-d", required=False, type=str, help="description of the tileset"
)
@click.option(
    "--privacy",
    "-p",
    required=False,
    type=click.Choice(["public", "private"]),
    help="set the tileset privacy options",
)
@click.option(
    "--attribution",
    required=False,
    type=str,
    help="attribution for the tileset in the form of a JSON string - Array<Object<text,link>>",
)
def update(
    tileset,
    token=None,
    indent=None,
    name=None,
    description=None,
    privacy=None,
    attribution=None,
):
    """Update a tileset's information.

    tilesets update <tileset_id>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/{1}?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    body = {}
    if name:
        body["name"] = name
    if description:
        body["description"] = description
    if privacy:
        body["private"] = True if privacy == "private" else False
    if attribution:
        try:
            body["attribution"] = json.loads(attribution)
        except:
            click.echo("Unable to parse attribution JSON")
            click.exit(1)

    r = s.patch(url, json=body)

    if r.status_code != 204:
        raise errors.TilesetsError(r.text)


@click.command("delete")
@click.argument("tileset", required=True, type=str)
@click.option("--force", "-f", is_flag=True, help="Circumvents confirmation prompt")
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def delete(tileset, token=None, indent=None, force=None):
    """Delete your tileset.

    tilesets delete <tileset_id>
    """

    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()

    if not force:
        val = click.prompt(
            'To confirm tileset deletion please enter the full tileset id "{0}"'.format(
                tileset
            ),
            type=str,
        )
        if val != tileset:
            raise click.ClickException(f"{val} does not match {tileset}. Aborted!")

    url = "{0}/tilesets/v1/{1}?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    r = s.delete(url)
    if r.status_code == 200 or r.status_code == 204:
        click.echo("Tileset deleted.")
    else:
        raise errors.TilesetsError(r.text)
