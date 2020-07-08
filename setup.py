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
    description=u"CLI for interacting with and preparing data for the Tilesets API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[],
    keywords="",
    author=u"Mapbox",
    author_email="sam@mapbox.com",
    url="https://github.com/mapbox/tilesets-cli",
    license="BSD-2",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    install_requires=[
        "boto3",
        "click~=7.0",
        "cligj",
        "requests",
        "requests-toolbelt",
        "jsonschema~=3.0",
        "jsonseq~=1.0",
    ],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        "test": ["pytest==4.6.11", "pytest-cov", "pre-commit", "black", "pep8"]
    },
    entry_points="""
      [console_scripts]
      tilesets=mapbox_tilesets.scripts.cli:cli
      """,
)
