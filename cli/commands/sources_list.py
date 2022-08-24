import json

import click
from cli.utils.common import token_option
from cli.utils.http import get_session


@click.command("list")
@click.option("--account", "-a", required=True, type=str)
@click.option("--limit", required=False, type=int)
@click.option(
    "--sortby",
    required=False,
    type=click.Choice(["modified", "created"]),
    default="modified",
)
@token_option
def list(account, limit, sortby, token):
    client = get_session(token)
    params = {}
    if limit:
        params["limit"] = limit
    response = client.get("/tilesets/v1/sources/{0}".format(account), params=params)
    click.echo(json.dumps(response.json()))
