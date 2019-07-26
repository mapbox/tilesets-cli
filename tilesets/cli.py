# Skeleton of a CLI

import os
import json
import sys

import click
import tilesets
import requests
from tilesets.scripts import uploader, utils
import jsonschema
from jsonseq.decode import JSONSeqDecoder
from json.decoder import JSONDecodeError

@click.version_option(version=tilesets.__version__, message='%(version)s')
@click.group()
def cli():
    """This is the command line interface for interacting with the Mapbox Tilesets API.
    Thanks for joining us.

    This CLI requires a Mapbox access token. You can either set it in your environment as
    "MAPBOX_ACCESS_TOKEN" or "MapboxAccessToken" or pass it to each command with the --token flag.
    """
@cli.command('validate-source')
@click.argument('source_path', required=True, type=click.Path(exists=True))
def validate_source(source_path):
    """Validate your source file.
    $ tilesets validate-source <path/to/your/src/file>
    """
    line_count = 1
    with open(source_path, 'r') as inf:
        click.echo("[validation] Scanning your file...")
        feature = None
        try:
            for feature in JSONSeqDecoder().decode(inf):
                utils.validate_geojson(feature)
                line_count+=1
        except JSONDecodeError:
            click.echo("Error: Invalid JSON on line {} \n Invalid Content: {} \n".format(line_count, feature))
            sys.exit(1)
        except jsonschema.exceptions.ValidationError:
            click.echo("Error: Invalid geojson found on line {} \n Invalid Feature: {} \n Note - Geojson must be line delimited.".format(line_count, feature))
            sys.exit(1)

    click.echo('Source file format and data are valid for file {}'.format(os.path.basename(source_path)))

@cli.command('create')
@click.argument('tileset', required=True, type=str)
@click.option('--recipe', '-r', required=True, type=click.Path(exists=True), help='path to a Recipe JSON document')
@click.option('--name', '-n', required=True, type=str, help='name of the tileset')
@click.option('--description', '-d', required=False, type=str, help='description of the tileset')
@click.option('--privacy', '-p', required=False, type=click.Choice(['public', 'private']), help='set the tileset privacy options')
@click.option('--token', '-t', required=False, type=str, help='Mapbox access token')
def create(tileset, recipe, name=None, description=None, privacy=None, token=None):
    """Create a new tileset with a recipe.

    $ tilesets create <tileset_id>

    <tileset_id> is in the form of username.handle - for example "mapbox.neat-tileset".
    The handle may only include "-" or "_" special characters.
    """
    mapbox_token = token if token is not None else tilesets.MAPBOX_TOKEN
    url = '{0}/tilesets/v1/{1}?access_token={2}'.format(tilesets.MAPBOX_API, tileset, mapbox_token)
    body = {}
    body['name'] = name or ''
    body['description'] = description or ''
    if privacy:
        body['private'] = True if privacy == 'private' else False

    if not '.' in tileset:
        click.echo('Invalid tileset_id, format must match username.tileset')
        sys.exit()

    if recipe:
        with open(recipe) as json_recipe:
            body['recipe'] = json.load(json_recipe)

    r = requests.post(url, json=body)
    utils.print_response(r.text)

@cli.command('upload')
@click.argument('tileset', required=True, type=str)
@click.argument('files', required=True, type=click.Path(exists=True, file_okay=True, dir_okay=True), nargs=-1)
@click.option('--no-validation', is_flag=True, help='Bypass source file validation')
@click.option('--token', '-t', required=False, type=str, help='Mapbox access token')
@click.pass_context
def upload(ctx, tileset, files, no_validation, token=None):
    """Add a file (or directory of files) to the tileset's current batch.

    tilesets upload <tileset_id> /path/to/file.geojson
    tilesets upload <tileset_id> /path/to/files
    """
    mapbox_token = token if token is not None else tilesets.MAPBOX_TOKEN
    url = '{0}/tilesets/v1/{1}/credentials?access_token={2}'.format(tilesets.MAPBOX_API, tileset, mapbox_token)

    for f in utils.flatten(files):
        if not no_validation:
            ctx.invoke(validate_source, source_path=f)
        r = requests.post(url)
        if r.status_code == 200:
            if r.json().message == 'Not Found':
                click.echo('Account not found.')
            else:
                uploader.upload(f, r.json())
                click.echo(f'Done staging files. You can publish these to a tileset with `tilesets publish {tileset}`')
        else:
            utils.print_response(r.text)

    click.echo(f'Done staging files. You can publish these to a tileset with `tilesets publish {tileset}`')


@cli.command('publish')
@click.argument('tileset', required=True, type=str)
@click.option('--token', '-t', required=False, type=str, help='Mapbox access token')
def publish(tileset, token=None):
    """Publish your tileset.

    tilesets publish <tileset_id>
    """
    mapbox_token = token if token is not None else tilesets.MAPBOX_TOKEN
    url = '{0}/tilesets/v1/{1}/publish?access_token={2}'.format(tilesets.MAPBOX_API, tileset, mapbox_token)
    r = requests.post(url)
    if r.status_code == 200:
        utils.print_response(r.text)
        click.echo(f'You can view the status of your tileset with the `tilesets status {tileset}` command.')
    else:
        utils.print_response(r.text)


@cli.command('status')
@click.argument('tileset', required=True, type=str)
@click.option('--token', '-t', required=False, type=str, help='Mapbox access token')
def status(tileset, token=None):
    """View the current queue/processing/complete status of your tileset.

    tilesets status <tileset_id>
    """
    mapbox_token = token if token is not None else tilesets.MAPBOX_TOKEN
    url = '{0}/tilesets/v1/{1}/status?access_token={2}'.format(tilesets.MAPBOX_API, tileset, mapbox_token)
    r = requests.get(url)
    utils.print_response(r.text)

@cli.command('jobs')
@click.argument('tileset', required=True, type=str)
@click.option('--stage', '-s', required=False, type=str, help='job stage')
def jobs(tileset, stage):
    """View the current queue/processing/complete status of your tileset.

    tilesets jobs <tileset_id>
    """

    url = '{0}/tilesets/v1/{1}/jobs?access_token={2}'.format(tilesets.MAPBOX_API, tileset, tilesets.MAPBOX_TOKEN)
    if stage:
        url = '{0}/tilesets/v1/{1}/jobs?stage={2}&access_token={3}'.format(tilesets.MAPBOX_API, tileset, stage, tilesets.MAPBOX_TOKEN)
    r = requests.get(url)
    utils.print_response(r.text)

@cli.command('job')
@click.argument('tileset', required=True, type=str)
@click.argument('job_id', required=True, type=str)
def job(tileset, job_id):
    """View the current queue/processing/complete status of your tileset.

    tilesets job <tileset_id> <job_id>
    """
    url = '{0}/tilesets/v1/{1}/jobs/{2}?access_token={3}'.format(tilesets.MAPBOX_API, tileset, job_id, tilesets.MAPBOX_TOKEN)
    r = requests.get(url)
    utils.print_response(r.text)


@cli.command('validate-recipe')
@click.argument('recipe', required=True, type=click.Path(exists=True))
@click.option('--token', '-t', required=False, type=str, help='Mapbox access token')
def validate_recipe(recipe, token=None):
    """Validate a Recipe JSON document

    tilesets validate-recipe <path_to_recipe>
    """
    mapbox_token = token if token is not None else tilesets.MAPBOX_TOKEN
    url = '{0}/tilesets/v1/validateRecipe?access_token={1}'.format(tilesets.MAPBOX_API, mapbox_token)
    with open(recipe) as json_recipe:
        try:
            recipe_json = json.load(json_recipe)
        except:
            click.echo('Error: recipe is not valid json')
            sys.exit()
        r = requests.put(url, json=recipe_json)
        utils.print_response(r.text)


@cli.command('view-recipe')
@click.argument('tileset', required=True, type=str)
@click.option('--token', '-t', required=False, type=str, help='Mapbox access token')
def view_recipe(tileset, token=None):
    """View a tileset's recipe JSON

    tilesets view-recipe <tileset_id>
    """
    mapbox_token = token if token is not None else tilesets.MAPBOX_TOKEN
    url = '{0}/tilesets/v1/{1}/recipe?access_token={2}'.format(tilesets.MAPBOX_API, tileset, mapbox_token)
    r = requests.get(url)
    if r.status_code == 200:
        utils.print_response(r.text)
    else:
        click.echo(r.text)


@cli.command('update-recipe')
@click.argument('tileset', required=True, type=str)
@click.argument('recipe', required=True, type=click.Path(exists=True))
@click.option('--token', '-t', required=False, type=str, help='Mapbox access token')
def update_recipe(tileset, recipe, token=None):
    """Update a Recipe JSON document for a particular tileset

    tilesets update-recipe <tileset_id> <path_to_recipe>
    """
    mapbox_token = token if token is not None else tilesets.MAPBOX_TOKEN
    url = '{0}/tilesets/v1/{1}/recipe?access_token={2}'.format(tilesets.MAPBOX_API, tileset, mapbox_token)
    with open(recipe) as json_recipe:
        try:
            recipe_json = json.load(json_recipe)
        except:
            click.echo('Error: recipe is not valid json')
            sys.exit()

        r = requests.patch(url, json=recipe_json)
        if r.status_code == 201:
            click.echo('Updated recipe.');
        else:
            utils.print_response(r.text)
