"""Changeset-related CLI commands."""

import json

import click
import cligj

from mapbox_tilesets import errors, utils
from mapbox_tilesets.scripts.cli_common import _upload_file, validate_source_id


@click.command("publish-changesets")
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


@click.command("view-changeset")
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


@click.command("delete-changeset")
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


@click.command("upload-changeset")
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
