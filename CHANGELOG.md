# Unreleased
- `update-recipe` command handles 204 status code in addition to 201 and no longer prints response text
- Add `update` command for updating `--name`, `--description`, `--privacy`, and `--attribution` of a tileset
- Add `--attribution` option to the `create` command

# 1.0.1.dev0 (2020-04-07)
- Fixed http status code for tilesets sources delete so it will no longer error

# 1.0.0.dev0 (2020-04-01)
- Rename package to mapbox-tilesets for pypi release

# 0.3.5 (2020-02-26)
- Add --force option to delete-sources

# 0.3.4 (2020-02-06)
- Stream add-source file upload with requests-toolbelt

# 0.3.3 (2020-01-16)
- Add confirmation prompt to delete-sources

# 0.3.2 (2019-10-08)
- Handling for non-json response from recipe validation
- Adding cligj to setup for install w/o requirements

# 0.3.1 (2019-10-01)
- Fixed bug for list tilesets

# 0.3.0 (2019-09-30)
- Feature input abstraction using `cligj`
- Logging refactor: default output is no compact JSON
- Informational printing (non-api responses) directed to stderr

## 0.2.1 (20190-09-16)
- Reformatting using `black`
- More robust tileset id checking

## 0.2.0 (2019-09-11)

- Add `tilesets list <account>` command

## 0.1.0 (2019-08-01)

- First release of the Mapbox Tilesets CLI :tada:
