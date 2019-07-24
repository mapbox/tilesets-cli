## Welcome

Hi there! Welcome to the tilesets-cli contributing document. Issues, comments, and pull requests are welcome. Please tag @mapsam, @dianeschulze, and @millzpaugh for any questions or reviews.

## Release process

Releases are simply tags on GitHub. Once changes have been merged to master:

1. Update the changelog
1. Tag on github with `git tag`. For example `git tag -a v0.2.0 -m 'v0.2.0'`

## Tests

All tests are runnable with pytest. pytest is not installed by default and can be installed with the pip test extras

```shell
pip install -e .[test]
```

Running tests

```
pytest
```
