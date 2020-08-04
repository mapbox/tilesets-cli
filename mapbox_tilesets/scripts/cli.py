"""Tilesets command line interface"""
import json
import tempfile

import click
import cligj
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

import mapbox_tilesets
from mapbox_tilesets import utils, errors


@click.version_option(version=mapbox_tilesets.__version__, message="%(version)s")
@click.group()
def cli():
    """This is the command line interface for the Mapbox Tilesets API.
    Thanks for joining us.

    This CLI requires a Mapbox access token. You can either set it in your environment as
    "MAPBOX_ACCESS_TOKEN" or "MapboxAccessToken" or pass it to each command with the --token flag.
    """


@cli.command("create")
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


@cli.command("publish")
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
        click.echo(json.dumps(r.json(), indent=indent))
        click.echo(
            f"You can view the status of your tileset with the `tilesets status {tileset}` command.",
            err=True,
        )
    else:
        raise errors.TilesetsError(r.text)


@cli.command("update")
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


@cli.command("delete")
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


@cli.command("status")
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
    url = "{0}/tilesets/v1/{1}/status?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    r = s.get(url)

    click.echo(json.dumps(r.json(), indent=indent))


@cli.command("tilejson")
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


@cli.command("jobs")
@click.argument("tileset", required=True, type=str)
@click.option("--stage", "-s", required=False, type=str, help="job stage")
@click.option(
    "--limit",
    required=False,
    type=click.IntRange(1, 500),
    default=100,
    help="The maximum number of results to return, from 1 to 500 (default 100)",
)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def jobs(tileset, stage=None, limit=None, token=None, indent=None):
    """View all jobs for a particular tileset.

    Only supports tilesets created with the Mapbox Tiling Service.

    tilesets jobs <tileset_id>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/{1}/jobs?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    url = "{0}&limit={1}".format(url, limit) if limit else url
    url = "{0}&stage={1}".format(url, stage) if stage else url
    r = s.get(url)
    click.echo(json.dumps(r.json(), indent=indent))


@cli.command("job")
@click.argument("tileset", required=True, type=str)
@click.argument("job_id", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def job(tileset, job_id, token=None, indent=None):
    """View a single job for a particular tileset.

    Only supports tilesets created with the Mapbox Tiling Service.

    tilesets job <tileset_id> <job_id>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/{1}/jobs/{2}?access_token={3}".format(
        mapbox_api, tileset, job_id, mapbox_token
    )
    r = s.get(url)

    click.echo(json.dumps(r.json(), indent=indent))


@cli.command("list")
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
    type=click.Choice(["vector", "raster"]),
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

    tilests list <username>
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


@cli.command("validate-recipe")
@click.argument("recipe", required=True, type=click.Path(exists=True))
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def validate_recipe(recipe, token=None, indent=None):
    """Validate a Recipe JSON document

    tilesets validate-recipe <path_to_recipe>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/validateRecipe?access_token={1}".format(
        mapbox_api, mapbox_token
    )
    with open(recipe) as json_recipe:
        recipe_json = json.load(json_recipe)

        r = s.put(url, json=recipe_json)
        click.echo(json.dumps(r.json(), indent=indent))


@cli.command("view-recipe")
@click.argument("tileset", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def view_recipe(tileset, token=None, indent=None):
    """View a tileset's recipe JSON

    tilesets view-recipe <tileset_id>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/{1}/recipe?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    r = s.get(url)
    if r.status_code == 200:
        click.echo(json.dumps(r.json(), indent=indent))
    else:
        raise errors.TilesetsError(r.text)


@cli.command("update-recipe")
@click.argument("tileset", required=True, type=str)
@click.argument("recipe", required=True, type=click.Path(exists=True))
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def update_recipe(tileset, recipe, token=None, indent=None):
    """Update a Recipe JSON document for a particular tileset

    Only supports tilesets created with the Mapbox Tiling Service.

    tilesets update-recipe <tileset_id> <path_to_recipe>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/{1}/recipe?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    with open(recipe) as json_recipe:
        recipe_json = json.load(json_recipe)

        r = s.patch(url, json=recipe_json)
        if r.status_code == 201 or r.status_code == 204:
            click.echo("Updated recipe.", err=True)
        else:
            raise errors.TilesetsError(r.text)


@cli.command("validate-source")
@cligj.features_in_arg
def validate_source(features):
    """Validate your source file.
    $ tilesets validate-source <path/to/your/src/file>
    """
    click.echo("Validating features", err=True)

    for feature in features:
        utils.validate_geojson(feature)

    click.echo("✔ valid")


@cli.command("upload-source")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
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
    return _upload_source(
        ctx, username, id, features, no_validation, quiet, replace, token, indent
    )


def _upload_source(
    ctx, username, id, features, no_validation, quiet, replace, token=None, indent=None
):
    """Create/add a tileset source

    tilesets add-source <username> <id> <path/to/source/data>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = (
        f"{mapbox_api}/tilesets/v1/sources/{username}/{id}?access_token={mapbox_token}"
    )

    method = "post"
    if replace:
        method = "put"

    with tempfile.TemporaryFile() as file:
        for feature in features:
            if not no_validation:
                utils.validate_geojson(feature)

            file.write(
                (json.dumps(feature, separators=(",", ":")) + "\n").encode("utf-8")
            )

        file.seek(0)
        m = MultipartEncoder(fields={"file": ("file", file)})

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


@cli.command("add-source")
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
    """Create/add/replace a tileset source

    tilesets add-source <username> <id> <path/to/source/data>
    """
    return _upload_source(
        ctx, username, id, features, no_validation, quiet, False, token, indent
    )


@cli.command("view-source")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def view_source(username, id, token=None, indent=None):
    """View a Tileset Source's information

    tilesets view-source <username> <id>
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


@cli.command("delete-source")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
@click.option("--force", "-f", is_flag=True, help="Circumvents confirmation prompt")
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def delete_source(username, id, force, token=None):
    """Delete a Tileset Source + all of its files.

    tilesets delete-source <username> <id>
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


@cli.command("list-sources")
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
