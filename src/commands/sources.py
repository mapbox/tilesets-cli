import click
from .sources_get import get
from .sources_list import list


@click.group()
def sources():
    pass


sources.add_command(get)
sources.add_command(list)
