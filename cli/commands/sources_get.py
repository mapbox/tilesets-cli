import json

import click
from cli.utils.common import token_option
from cli.utils.http import get_session


@click.command("get")
@click.option("--id", required=True, type=str)
@token_option
def get(id, token):
    account, id = id.split("/")
    client = get_session(token)
    response = client.get("/tilesets/v1/sources/{0}/{1}".format(account, id))
    click.echo(json.dumps(response.json()))
