"""Shared CLI helpers."""

import base64
import json
import re
import tempfile

import click
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from mapbox_tilesets import errors, utils


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


def _upload_file(
    ctx,
    username,
    id,
    features,
    no_validation,
    quiet,
    replace,
    changeset,
    token=None,
    indent=None,
):
    api_endpoint = "changesets" if changeset else "sources"

    mapbox_api = utils._get_api()
    mapbox_token = utils._get_token(token)
    s = utils._get_session()
    url = f"{mapbox_api}/tilesets/v1/{api_endpoint}/{username}/{id}?access_token={mapbox_token}"

    method = "post"
    if replace:
        method = "put"

    # This does the decoding by hand instead of using pyjwt because
    # pyjwt rejects tokens that don't pad the base64 with = signs.
    token_parts = mapbox_token.split(".")
    if len(token_parts) < 2:
        raise errors.TilesetsError(
            f"Token {mapbox_token} does not contain a payload component"
        )
    else:
        while len(token_parts[1]) % 4 != 0:
            token_parts[1] = token_parts[1] + "="
        body = json.loads(base64.b64decode(token_parts[1]))
        if "u" in body:
            if username != body["u"]:
                raise errors.TilesetsError(
                    f"Token username {body['u']} does not match username {username}"
                )
        else:
            raise errors.TilesetsError(
                f"Token {mapbox_token} does not contain a username"
            )

    with tempfile.TemporaryFile() as file:
        for index, feature in enumerate(features):
            if not no_validation:
                utils.validate_geojson(index, feature, changeset)

            file.write(
                (json.dumps(feature, separators=(",", ":")) + "\n").encode("utf-8")
            )

        file.seek(0)
        m = MultipartEncoder(fields={"file": ("file", file)})

        if quiet:
            resp = getattr(s, method)(
                url,
                data=m,
                headers={
                    "Content-Disposition": "multipart/form-data",
                    "Content-type": m.content_type,
                },
            )
        else:
            prog = click.progressbar(
                length=m.len, fill_char="=", width=0, label="upload progress"
            )
            with prog:

                def callback(m):
                    prog.pos = m.bytes_read
                    prog.update(0)  # Step is 0 because we set pos above

                monitor = MultipartEncoderMonitor(m, callback)
                resp = getattr(s, method)(
                    url,
                    data=monitor,
                    headers={
                        "Content-Disposition": "multipart/form-data",
                        "Content-type": monitor.content_type,
                    },
                )

    if resp.status_code == 200:
        click.echo(json.dumps(resp.json(), indent=indent))
    else:
        raise errors.TilesetsError(resp.text)
