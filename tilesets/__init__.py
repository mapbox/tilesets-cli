# tilesets-cli

import os

__version__ = '0.1.0'

MAPBOX_API = (os.environ.get('MAPBOX_API') or
              'https://api.mapbox.com')
MAPBOX_TOKEN = (os.environ.get('MAPBOX_ACCESS_TOKEN') or
                os.environ.get('MapboxAccessToken'))
