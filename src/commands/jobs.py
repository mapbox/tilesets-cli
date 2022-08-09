import click
from .jobs_get import get


@click.group()
def jobs():
    pass


jobs.add_command(get)
