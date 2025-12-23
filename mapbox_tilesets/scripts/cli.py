"""Tilesets command line interface"""

import json
import re
from urllib.parse import parse_qs, urlencode, urlparse

import click

import mapbox_tilesets
from mapbox_tilesets import errors, utils
from mapbox_tilesets.scripts.cli_changesets import (
    delete_changeset,
    publish_changesets,
    upload_changeset,
    view_changeset,
)
from mapbox_tilesets.scripts.cli_jobs import job, jobs
from mapbox_tilesets.scripts.cli_recipes import (
    update_recipe,
    validate_recipe,
    view_recipe,
)
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
from mapbox_tilesets.scripts.cli_tilesets import (
    create,
    delete,
    list,
    publish,
    status,
    tilejson,
    update,
)


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
cli.add_command(create)
cli.add_command(publish)
cli.add_command(update)
cli.add_command(delete)
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
cli.add_command(validate_recipe)
cli.add_command(view_recipe)
cli.add_command(update_recipe)
cli.add_command(publish_changesets)
cli.add_command(view_changeset)
cli.add_command(delete_changeset)
cli.add_command(upload_changeset)


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
