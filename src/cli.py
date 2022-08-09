import click
from . import __version__
from .commands.tilesets import tilesets
from .commands.sources import sources
from .commands.jobs import jobs


@click.version_option(version=__version__, message="%(version)s")
@click.group()
def cli():
    """This is the command line interface for the Mapbox Tiling Service.

    This CLI requires a Mapbox access token. You can either set it in your environment as
    "MAPBOX_ACCESS_TOKEN" or "MapboxAccessToken" or pass it to each command with the --token flag.
    """
    pass


cli.add_command(tilesets)
cli.add_command(sources)
cli.add_command(jobs)
