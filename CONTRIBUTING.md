## Welcome

Hi there! Welcome to the tilesets-cli contributing document. Issues, comments, and pull requests are welcome. Please tag @mapsam, @dianeschulze, and @dnomadb for any questions or reviews.

## Installation
First, clone the repo and `cd` into the folder:
```shell
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
```
$ pre-commit install
```
within the repo to have the actions specified in `.pre-commit-config.yaml` registered.

After this, when committing, you'll see:
```
git commit -m 'update version'
black....................................................................Passed
Flake8...................................................................Passed
```
If your pre-commit hooks ran successfully. Note that `black` modifies your code, which means that if there is a syntax error you'll first see something like:
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

this/file/was/reformatted.py:{line}:{character}: {what was incorrect}
```
After which you can add these changes and commit again. Note that failing pre-commit commands mean that the commit has not taken place: you must commit again!

## Release process

Releases to PyPi are handled via TravisCI and GitHub tags. Once changes have been merged to master:

1. Update the version in tilesets/__init__.py
2. Update the changelog
3. Commit changes to **your branch**. For example `git commit -am '0.2.0' && git push origin HEAD`
4. Get a review and merge your changes to master.
5. Get the latest changes locally from master `git checkout master && git pull origin master`
6. Tag on GitHub with `git tag` and push tags. For example `git tag -a v0.2.0 -m 'v0.2.0' && git push --tags`
7. Watch for tag build on travis at https://travis-ci.com/github/mapbox/tilesets-cli/builds
8. Once travis completes successfully, look for the release at https://pypi.org/project/mapbox-tilesets/#history

## Tests

All tests are runnable with pytest. pytest is not installed by default and can be installed with the pip test extras

```shell
pip install -e .[test]
```

Running tests

```
pytest
```
