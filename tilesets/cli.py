"""Tilesets command line interface"""

import os
import json
import sys

import click
import tilesets
import requests
from tilesets.scripts import utils
import jsonschema
from jsonseq.decode import JSONSeqDecoder
from json.decoder import JSONDecodeError


def _get_token(token=None):
    """Get Mapbox access token from arg or environment"""
    if token is not None:
        return token
    else:
        return os.environ.get("MAPBOX_ACCESS_TOKEN") or os.environ.get(
            "MapboxAccessToken"
        )


def _get_api():
    """Get Mapbox tileset API base URL from environment"""
    return os.environ.get("MAPBOX_API", "https://api.mapbox.com")


@click.version_option(version=tilesets.__version__, message="%(version)s")
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
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def create(tileset, recipe, name=None, description=None, privacy=None, token=None):
    """Create a new tileset with a recipe.

    $ tilesets create <tileset_id>

    <tileset_id> is in the form of username.handle - for example "mapbox.neat-tileset".
    The handle may only include "-" or "_" special characters.
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/{1}?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    body = {}
    body["name"] = name or ""
    body["description"] = description or ""
    if privacy:
        body["private"] = True if privacy == "private" else False

    if utils.validate_tileset_id(tileset):
        click.echo("Invalid tileset_id, format must match username.tileset")
        sys.exit()

    if recipe:
        with open(recipe) as json_recipe:
            body["recipe"] = json.load(json_recipe)

    r = requests.post(url, json=body)
    utils.print_response(r.text)


@cli.command("publish")
@click.argument("tileset", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def publish(tileset, token=None):
    """Publish your tileset.

    tilesets publish <tileset_id>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/{1}/publish?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    r = requests.post(url)
    if r.status_code == 200:
        utils.print_response(r.text)
        click.echo(
            f"You can view the status of your tileset with the `tilesets status {tileset}` command."
        )
    else:
        utils.print_response(r.text)


@cli.command("status")
@click.argument("tileset", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def status(tileset, token=None):
    """View the current queue/processing/complete status of your tileset.

    tilesets status <tileset_id>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/{1}/status?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    r = requests.get(url)
    utils.print_response(r.text)


@cli.command("jobs")
@click.argument("tileset", required=True, type=str)
@click.option("--stage", "-s", required=False, type=str, help="job stage")
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def jobs(tileset, stage, token=None):
    """View all jobs for a particular tileset.

    tilesets jobs <tileset_id>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/{1}/jobs?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    if stage:
        url = "{0}/tilesets/v1/{1}/jobs?stage={2}&access_token={3}".format(
            mapbox_api, tileset, stage, mapbox_token
        )
    r = requests.get(url)
    utils.print_response(r.text)


@cli.command("job")
@click.argument("tileset", required=True, type=str)
@click.argument("job_id", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def job(tileset, job_id, token=None):
    """View a single job for a particular tileset.

    tilesets job <tileset_id> <job_id>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/{1}/jobs/{2}?access_token={3}".format(
        mapbox_api, tileset, job_id, mapbox_token
    )
    r = requests.get(url)
    utils.print_response(r.text)


@cli.command("list")
@click.argument("username", required=True, type=str)
@click.option(
    "--verbose",
    "-v",
    required=False,
    is_flag=True,
    help="Will print all tileset information",
)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def list(username, verbose, token=None):
    """List all tilesets for an account.
    By default the response is a simple list of tileset IDs.
    If you would like an array of all tileset's information,
    use the --versbose flag.

    tilests list <username>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/{1}?access_token={2}".format(
        mapbox_api, username, mapbox_token
    )
    r = requests.get(url)
    if r.status_code == 200:
        if verbose:
            utils.print_response(r.text)
        else:
            j = json.loads(r.text)
            for tileset in j:
                click.echo(tileset["id"])
    else:
        click.echo(r.text)


@cli.command("validate-recipe")
@click.argument("recipe", required=True, type=click.Path(exists=True))
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def validate_recipe(recipe, token=None):
    """Validate a Recipe JSON document

    tilesets validate-recipe <path_to_recipe>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/validateRecipe?access_token={1}".format(
        mapbox_api, mapbox_token
    )
    with open(recipe) as json_recipe:
        try:
            recipe_json = json.load(json_recipe)
        except:
            click.echo("Error: recipe is not valid json")
            sys.exit()
        r = requests.put(url, json=recipe_json)
        utils.print_response(r.text)


@cli.command("view-recipe")
@click.argument("tileset", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def view_recipe(tileset, token=None):
    """View a tileset's recipe JSON

    tilesets view-recipe <tileset_id>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/{1}/recipe?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    r = requests.get(url)
    if r.status_code == 200:
        utils.print_response(r.text)
    else:
        click.echo(r.text)


@cli.command("update-recipe")
@click.argument("tileset", required=True, type=str)
@click.argument("recipe", required=True, type=click.Path(exists=True))
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def update_recipe(tileset, recipe, token=None):
    """Update a Recipe JSON document for a particular tileset

    tilesets update-recipe <tileset_id> <path_to_recipe>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/{1}/recipe?access_token={2}".format(
        mapbox_api, tileset, mapbox_token
    )
    with open(recipe) as json_recipe:
        try:
            recipe_json = json.load(json_recipe)
        except:
            click.echo("Error: recipe is not valid json")
            sys.exit()

        r = requests.patch(url, json=recipe_json)
        if r.status_code == 201:
            click.echo("Updated recipe.")
        else:
            utils.print_response(r.text)


@cli.command("validate-source")
@click.argument("source_path", required=True, type=click.Path(exists=True))
def validate_source(source_path):
    """Validate your source file.
    $ tilesets validate-source <path/to/your/src/file>
    """
    line_count = 1
    with open(source_path, "r") as inf:
        click.echo("Validating {0} ...".format(source_path))
        feature = None
        try:
            for feature in JSONSeqDecoder().decode(inf):
                utils.validate_geojson(feature)
                line_count += 1
        except JSONDecodeError:
            click.echo(
                "Error: Invalid JSON on line {} \n Invalid Content: {} \n".format(
                    line_count, feature
                )
            )
            sys.exit(1)
        except jsonschema.exceptions.ValidationError:
            click.echo(
                "Error: Invalid geojson found on line {} \n Invalid Feature: {} \n Note - Geojson must be line delimited.".format(
                    line_count, feature
                )
            )
            sys.exit(1)

    click.echo("✔ valid")


@cli.command("add-source")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
@click.argument(
    "files",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
    nargs=-1,
)
@click.option("--no-validation", is_flag=True, help="Bypass source file validation")
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
@click.pass_context
def add_source(ctx, username, id, files, no_validation, token=None):
    """Create/add a tileset source

    tilesets add-source <username> <id> <path/to/source/data>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    for f in utils.flatten(files):
        url = "{0}/tilesets/v1/sources/{1}/{2}?access_token={3}".format(
            mapbox_api, username, id, mapbox_token
        )
        if not no_validation:
            ctx.invoke(validate_source, source_path=f)

        click.echo(
            "Adding {0} to mapbox://tileset-source/{1}/{2}".format(f, username, id)
        )

        r = requests.post(url, files={"file": ("tileset-source", open(f, "rb"))})

        if r.status_code == 200:
            utils.print_response(r.text)
        else:
            click.echo(r.text)


@cli.command("view-source")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def view_source(username, id, token=None):
    """View a Tileset Source's information

    tilesets view-source <username> <id>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/sources/{1}/{2}?access_token={3}".format(
        mapbox_api, username, id, mapbox_token
    )
    r = requests.get(url)
    if r.status_code == 200:
        utils.print_response(r.text)
    else:
        click.echo(r.text)


@cli.command("delete-source")
@click.argument("username", required=True, type=str)
@click.argument("id", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def delete_source(username, id, token=None):
    """Delete a Tileset Source + all of its files.

    tilesets delete-source <username> <id>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/sources/{1}/{2}?access_token={3}".format(
        mapbox_api, username, id, mapbox_token
    )
    r = requests.delete(url)
    if r.status_code == 201:
        click.echo("Source deleted.")
    else:
        utils.print_response(r.text)


@cli.command("list-sources")
@click.argument("username", required=True, type=str)
@click.option("--token", "-t", required=False, type=str, help="Mapbox access token")
def list_sources(username, token=None):
    """List all Tileset Sources for an account. Response is an un-ordered array of sources.

    tilesets list-sources <username>
    """
    mapbox_api = _get_api()
    mapbox_token = _get_token(token)
    url = "{0}/tilesets/v1/sources/{1}?access_token={2}".format(
        mapbox_api, username, mapbox_token
    )
    r = requests.get(url)
    if r.status_code == 200:
        utils.print_response(r.text)
    else:
        click.echo(r.text)
