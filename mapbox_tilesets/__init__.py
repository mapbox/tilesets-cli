"""mapbox_tilesets package"""

from importlib.metadata import PackageNotFoundError, version as _pkg_version

try:
    __version__ = _pkg_version("mapbox-tilesets")
except PackageNotFoundError:
    __version__ = "0.0.0"
