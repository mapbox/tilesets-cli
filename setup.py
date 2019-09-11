import os
from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open("README.md", encoding="utf-8") as f:
    long_description = f.read()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="tilesets-cli",
    version="0.2.0",
    description=u"CLI for interacting with and preparing data for the Tilesets API",
    long_description=long_description,
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
        "requests",
        "jsonschema~=3.0",
        "jsonseq~=1.0",
    ],
    include_package_data=True,
    zip_safe=False,
    extras_require={"test": ["pytest>=3.6.0", "pytest-cov", "pre-commit"]},
    entry_points="""
      [console_scripts]
      tilesets=tilesets.cli:cli
      """,
)
