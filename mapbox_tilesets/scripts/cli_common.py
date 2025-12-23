"""Shared CLI helpers."""

import re

import click

from mapbox_tilesets import utils


def validate_source_id(ctx, param, value):
    if re.match("^[a-zA-Z0-9-_]{1,32}$", value):
        return value
    raise click.BadParameter(
        'Tileset Source ID is invalid. Must be no more than 32 characters and only include "-", "_", and alphanumeric characters.'
    )


def validate_stream(features):
    for index, feature in enumerate(features):
        utils.validate_geojson(index, feature)
        yield feature
