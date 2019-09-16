## Welcome

Hi there! Welcome to the tilesets-cli contributing document. Issues, comments, and pull requests are welcome. Please tag @mapsam, @dianeschulze, and @millzpaugh for any questions or reviews.

## Release process

Releases are simply tags on GitHub. Once changes have been merged to master:

1. Update the changelog
1. Tag on github with `git tag`. For example `git tag -a v0.2.0 -m 'v0.2.0'`

## Installation
First, clone the repo and `cd` into the folder:
```
$ git clone git@github.com:mapbox/tilesets-cli.git
$ cd tilesets-cli
```
Then, in a virtual environment, install the module with `[test]` extras:
```
pip install -e '.[test]'
```
## Pre-commit hooks
We use [pre-commit hooks](https://pre-commit.com/) to auto-format and validate code before committing. `pre-commit` is included with the `[test]` extras, but you must run:
```
$ pre-commit install
```
within the repo to have the actions specified in `.pre-commit-config.yaml`.

After this, when commit, you'll see:
```
git commit -m 'update version'
black....................................................................Passed
Flake8...................................................................Passed
```
If your pre-commit hooks ran successfully. Note that `black` modifies your code, which means that if there is a syntax error you'll first see:
```
git commit -m '{message}'
black....................................................................Failed
hookid: black

Files were modified by this hook. Additional output:

reformatted this/file/was/reformatted.py
All done! ✨ 🍰 ✨
1 file reformatted.

Flake8...................................................................Failed
hookid: flake8

this/file/was/reformatted.py:{line}:{character}: {what is incorrect}
```

## Tests

All tests are runnable with pytest. pytest is not installed by default and can be installed with the pip test extras

```shell
pip install -e .[test]
```

Running tests

```
pytest
```
