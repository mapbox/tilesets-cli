import json

import click
from cli.utils.http import get_session


@click.command("get")
@click.option("--id", required=True, type=str, help="Tileset ID")
@click.option("--token", required=False, type=str)
def get(id, token):
    client = get_session(token)
    response = client.get("/tilesets/v1/{0}".format(id))
    click.echo(json.dumps(response.json()))
