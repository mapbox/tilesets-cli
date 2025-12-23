"""Tilesets command line interface"""

import json
import re
from urllib.parse import parse_qs, urlencode, urlparse

import click
import cligj

import mapbox_tilesets
from mapbox_tilesets import errors, utils
from mapbox_tilesets.scripts.cli_common import _upload_file, validate_source_id
from mapbox_tilesets.scripts.cli_jobs import job, jobs
from mapbox_tilesets.scripts.cli_sources import (
    add_source,
    delete_source,
    estimate_area,
    list_sources,
    upload_raster_source,
    upload_source,
    validate_source,
    view_source,
)
from mapbox_tilesets.scripts.cli_tilesets import list, status, tilejson


@click.version_option(version=mapbox_tilesets.__version__, message="%(version)s")
@click.group()
def cli():
    """This is the command line interface for the Mapbox Tilesets API.
    Thanks for joining us.

    This CLI requires a Mapbox access token. You can either set it in your environment as
    "MAPBOX_ACCESS_TOKEN" or "MapboxAccessToken" or pass it to each command with the --token flag.
    """


cli.add_command(status)
cli.add_command(tilejson)
cli.add_command(list)
cli.add_command(jobs)
cli.add_command(job)
cli.add_command(validate_source)
cli.add_command(upload_source)
cli.add_command(upload_raster_source)
cli.add_command(add_source)
cli.add_command(view_source)
cli.add_command(delete_source)
cli.add_command(list_sources)
cli.add_command(estimate_area)


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
        response_msg = r.json()
        click.echo(json.dumps(response_msg, indent=indent))

        studio_url = click.style(
            f"https://studio.mapbox.com/tilesets/{tileset}", bold=True
        )
        job_id = response_msg["jobId"]
        job_cmd = click.style(f"tilesets job {tileset} {job_id}", bold=True)
        message = f"\n✔ Tileset job received. Visit {studio_url} or run {job_cmd} to view the status of your tileset."
        # print(message)
        click.echo(
            message,
            err=True,  # print to stderr so the JSON output can be parsed separately from the success message
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


@cli.command("list-activity")
@click.argument("username", required=True, type=str)
@click.option(
    "--sortby",
    required=False,
    type=click.Choice(["requests", "modified"]),
    default="requests",
    help="Sort the results by request count or modified timestamps (default: 'requests')",
)
@click.option(
    "--orderby",
    required=False,
    type=click.Choice(["asc", "desc"]),
    default="desc",
    help="Order results by asc or desc for the sort key (default: 'desc')",
)
@click.option(
    "--limit",
    required=False,
    type=click.IntRange(1, 500),
    default=100,
    help="The maximum number of results to return, from 1 to 500 (default: 100)",
)
@click.option(
    "--start",
    required=False,
    type=str,
    help="Pagination key from the `next` value in a response that has more results than the limit.",
)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def list_activity(
    username,
    sortby=None,
    orderby=None,
    limit=None,
    start=None,
    token=None,
    indent=None,
):
    """List tileset activity for an account. The response is an ordered array of data about the user's tilesets and their
    total requests over the past 30 days. The sorting and ordering can be configured through cli arguments, defaulting to
    descending request counts.

    tilesets list-activity <username>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()

    params = {
        "access_token": mapbox_token,
        "sortby": sortby,
        "orderby": orderby,
        "limit": limit,
        "start": start,
    }
    params = {k: v for k, v in params.items() if v}
    query_string = urlencode(params)
    url = f"{mapbox_api}/activity/v1/{username}/tilesets?{query_string}"

    r = s.get(url)
    if r.status_code == 200:
        if r.headers.get("Link"):
            url = re.findall(r"<(.*)>;", r.headers.get("Link"))[0]
            query = urlparse(url).query
            start = parse_qs(query)["start"][0]

        result = {
            "data": r.json(),
            "next": start,
        }
        click.echo(json.dumps(result, indent=indent))
    else:
        raise errors.TilesetsError(r.text)


@cli.command("publish-changesets")
@click.argument("tileset_id", required=True, type=str)
@click.argument("changeset_payload", required=True, type=click.Path(exists=True))
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def publish_changesets(tileset_id, changeset_payload, token=None, indent=None):
    """Publish changesets for a tileset.

    tilesets publish-changesets <tileset_id> <path_to_changeset_payload>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/{1}/publish-changesets?access_token={2}".format(
        mapbox_api, tileset_id, mapbox_token
    )
    with open(changeset_payload) as changeset_payload_content:
        changeset_payload_json = json.load(changeset_payload_content)

        r = s.post(url, json=changeset_payload_json)
        if r.status_code == 200:
            response_msg = r.json()
            click.echo(json.dumps(response_msg, indent=indent))
        else:
            raise errors.TilesetsError(r.text)


@cli.command("view-changeset")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
def view_changeset(username, id, token=None, indent=None):
    """View a Changeset's information

    tilesets view-changeset <username> <changeset_id>
    """
    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = "{0}/tilesets/v1/changesets/{1}/{2}?access_token={3}".format(
        mapbox_api, username, id, mapbox_token
    )
    r = s.get(url)
    if r.status_code == 200:
        click.echo(json.dumps(r.json(), indent=indent))
    else:
        raise errors.TilesetsError(r.text)


@cli.command("delete-changeset")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
@click.option("--force", "-f", is_flag=True, help="Circumvents confirmation prompt")
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def delete_changeset(username, id, force, token=None):
    """Permanently delete a changeset and all of its files

    tilesets delete-changeset <username> <changeset_id>
    """
    if not force:
        val = click.prompt(
            'To confirm changeset deletion please enter the full changeset id "{0}/{1}"'.format(
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
    url = "{0}/tilesets/v1/changesets/{1}/{2}?access_token={3}".format(
        mapbox_api, username, id, mapbox_token
    )
    r = s.delete(url)
    if r.status_code == 204:
        click.echo("Changeset deleted.")
    else:
        raise errors.TilesetsError(r.text)


@cli.command("upload-changeset")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, callback=validate_source_id, type=str)
@cligj.features_in_arg
@click.option("--no-validation", is_flag=True, help="Bypass changeset file validation")
@click.option("--quiet", is_flag=True, help="Don't show progress bar")
@click.option(
    "--replace",
    is_flag=True,
    help="Replace the existing changeset with the new changeset file",
)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.option("--indent", type=int, default=None, help="Indent for JSON output")
@click.pass_context
def upload_changeset(
    ctx, username, id, features, no_validation, quiet, replace, token=None, indent=None
):
    """Create a new changeset, or add data to an existing changeset.
    Optionally, replace an existing changeset.

    tilesets upload-changeset <username> <source_id> <path/to/changeset/data>
    """
    return _upload_file(
        ctx, username, id, features, no_validation, quiet, replace, True, token, indent
    )
