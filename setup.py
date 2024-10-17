import os
from codecs import open as codecs_open
from setuptools import setup, find_packages

from mapbox_tilesets import __version__

# Get the long description from the relevant file
with codecs_open("README.md", encoding="utf-8") as f:
    long_description = f.read()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="mapbox-tilesets",
    version=__version__,
    description="CLI for interacting with and preparing data for the Tilesets API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[],
    keywords="",
    author="Mapbox",
    author_email="sam@mapbox.com",
    url="https://github.com/mapbox/tilesets-cli",
    license="BSD-2",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    install_requires=[
        "boto3",
        "click~=8.0.2",
        "cligj",
        "numpy",
        "requests",
        "requests-toolbelt",
        "jsonschema~=3.0",
        "jsonseq~=1.0",
        "mercantile~=1.1.6",
        "geojson~=2.5.0",
    ],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        "estimate-area": [
            "supermercado~=0.2.0",
        ],
        "estimate-cu": [
            "rasterio~=1.4.1",
        ],
        "test": [
            "codecov",
            "pytest==6.2.5",
            "pytest-cov",
            "pre-commit",
            "black==22.3.0",
            "pep8",
            "supermercado~=0.2.0",
            "toml==0.10.2",
        ],
    },
    entry_points="""
      [console_scripts]
      tilesets=mapbox_tilesets.scripts.cli:cli
      """,
)
