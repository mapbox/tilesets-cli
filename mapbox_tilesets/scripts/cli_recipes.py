"""Recipe-related CLI commands."""

import json

import click

from mapbox_tilesets import errors, utils


@click.command("validate-recipe")
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


@click.command("view-recipe")
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


@click.command("update-recipe")
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
