import os

from requests_toolbelt.sessions import BaseUrlSession

import cli


def get_session(token=None):
    """Get a configured Session with user-agent headers and a Mapbox access token"""
    token = (
        token
        or os.environ.get("MAPBOX_ACCESS_TOKEN")
        or os.environ.get("MapboxAccessToken")
    )

    if token is None:
        raise cli.errors.TilesetsError(
            "No access token provided. Please set the MAPBOX_ACCESS_TOKEN environment variable or use the --token flag."
        )

    base = os.environ.get("MAPBOX_API", "https://api.mapbox.com")
    session = BaseUrlSession(base)
    session.params.update({"access_token": token})
    session.headers.update(
        {"user-agent": "{}/{}".format(cli.__name__, cli.__version__)}
    )
    return session
