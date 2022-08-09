import click


@click.command()
def list():
    click.echo("This is the list subcommand of the tilesets command")
