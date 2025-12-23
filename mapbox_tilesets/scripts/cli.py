"""Tilesets command line interface"""

import click

import mapbox_tilesets
from mapbox_tilesets.scripts.cli_activity import list_activity
from mapbox_tilesets.scripts.cli_changesets import (
    delete_changeset,
    publish_changesets,
    upload_changeset,
    view_changeset,
)
from mapbox_tilesets.scripts.cli_jobs import job, jobs
from mapbox_tilesets.scripts.cli_recipes import (
    update_recipe,
    validate_recipe,
    view_recipe,
)
from mapbox_tilesets.scripts.cli_sources import (
    add_source,
    delete_source,
    estimate_area,
    list_sources,
    upload_raster_source,
    upload_source,
    validate_source,
    view_source,
)
from mapbox_tilesets.scripts.cli_tilesets import (
    create,
    delete,
    list,
    publish,
    status,
    tilejson,
    update,
)


@click.version_option(version=mapbox_tilesets.__version__, message="%(version)s")
@click.group()
def cli():
    """This is the command line interface for the Mapbox Tilesets API.
    Thanks for joining us.

    This CLI requires a Mapbox access token. You can either set it in your environment as
    "MAPBOX_ACCESS_TOKEN" or "MapboxAccessToken" or pass it to each command with the --token flag.
    """


# Tilesets
cli.add_command(status)
cli.add_command(tilejson)
cli.add_command(list)
cli.add_command(create)
cli.add_command(publish)
cli.add_command(update)
cli.add_command(delete)

# Jobs
cli.add_command(jobs)
cli.add_command(job)

# Sources
cli.add_command(validate_source)
cli.add_command(upload_source)
cli.add_command(upload_raster_source)
cli.add_command(add_source)
cli.add_command(view_source)
cli.add_command(delete_source)
cli.add_command(list_sources)
cli.add_command(estimate_area)

# Recipes
cli.add_command(validate_recipe)
cli.add_command(view_recipe)
cli.add_command(update_recipe)

# Changesets
cli.add_command(publish_changesets)
cli.add_command(view_changeset)
cli.add_command(delete_changeset)
cli.add_command(upload_changeset)

# Activity
cli.add_command(list_activity)
