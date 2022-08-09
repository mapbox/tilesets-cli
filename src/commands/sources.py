import click
from .sources_get import get


@click.group()
def sources():
    pass


sources.add_command(get)
