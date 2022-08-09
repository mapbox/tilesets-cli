import json

import click
from src.utils.http import get_session


@click.command("list")
@click.option("--account", required=True, type=str)
@click.option("--token", required=False, type=str)
def list(account, token):
    client = get_session(token)
    response = client.get("/tilesets/v1/sources/{0}".format(account))
    click.echo(json.dumps(response.json()))
