import click


@click.command()
def get():
    click.echo("This is the get subcommand of the jobs command")
