"""Job-related CLI commands."""

import json

import click

from mapbox_tilesets import utils


@click.command("jobs")
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


@click.command("job")
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
