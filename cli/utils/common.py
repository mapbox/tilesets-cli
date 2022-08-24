import click

token_option = click.option(
    "--token", "-t", required=False, type=str, help="Mapbox access token"
)
