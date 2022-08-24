import click
from .tilesets_get import get
from .tilesets_list import list
from .tilesets_create import create


@click.group()
def tilesets():
    pass


tilesets.add_command(get)
tilesets.add_command(list)
tilesets.add_command(create)
