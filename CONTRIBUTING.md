## Welcome

Hi there! Welcome to the tilesets-cli contributing document. Issues, comments, and pull requests are welcome. Please tag @mapbox/maps-api for any questions or reviews.

## Installation

First, clone the repo and `cd` into the folder:

```bash
# clone
git clone git@github.com:mapbox/tilesets-cli.git
cd tilesets-cli

# virtual env (optional)
mkvirtualenv tilesets-cli

# install deps
pip install -e '.[test]'

# confirm installation was successful
tilesets --help
tilesets --version
```

## Pre-commit hooks

We use [pre-commit hooks](https://pre-commit.com/) to auto-format and validate code before committing. `pre-commit` is included with the `[test]` extras, but you must run:

```bash
$ pre-commit install
```
within the repo to have the actions specified in `.pre-commit-config.yaml` registered.


## Release process

Releases to PyPi are handled via Github Actions and GitHub tags. Once changes have been merged to master:

1. Update the version in `pyproject.toml`
2. Update the changelog
3. Commit changes to **your branch**. For example `git commit -am '0.2.0' && git push origin HEAD`
4. Get a review and merge your changes to master.
5. Get the latest changes locally from master `git checkout master && git pull origin master`
6. Tag on GitHub with `git tag` and push tags. For example `git tag -a v0.2.0 -m 'v0.2.0' && git push --tags`
7. Watch for tag build on Github Actions at https://github.com/mapbox/tilesets-cli/actions
8. Once Github Actions completes successfully, look for the release at https://pypi.org/project/mapbox-tilesets/#history

## Tests

All tests are runnable with pytest. pytest is not installed by default and can be installed with the pip test extras

```shell
pip install -e '.[test]'
```

Running tests

```
pytest
```
