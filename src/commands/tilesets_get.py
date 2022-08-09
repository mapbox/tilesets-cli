import json

import click
from src.utils.http import get_session


@click.command("get")
@click.option("--id", required=True, type=str)
@click.option("--token", required=False, type=str)
def get(id, token):
    client = get_session(token)
    response = client.get("/tilesets/v1/{0}".format(id))
    click.echo(json.dumps(response.json()))
