# Unreleased

=======

# 1.11.0 (2024-08-01)
- Added command `tilesets upload-raster-source` to upload raster files as sources

# 1.10.0 (2024-05-07)
- Add support for the `rasterarray` type on the `list` command.

# 1.9.3 (2023-06-27)
- Beautified error messages

# 1.9.2 (2023-06-21)
- Use Bionic dist instead of Xenial for Travis build

# 1.9.1 (2023-06-21)
- Pin urllib3 version, see: https://github.com/urllib3/urllib3/issues/2168

# 1.9.0 (2023-06-14)
- Added command `tilesets list-activity` that returns activity data for a user's tilesets

# 1.8.1 (2022-08-29)
- Bug Fix: Fix setup script to have `geojson` package in setup.py install requirements

# 1.8.0 (2022-08-25) - [YANKED]

*Yanked due to missing `geojson` package in setup.py*

- Validates source in `upload-source` command using [geojson package](https://github.com/jazzband/geojson).
- Provides line number for an invalid feature that is detected with the geojson validator.

# 1.7.4 (2022-07-13)
- Validates source id for correct syntax when `upload-source` command to resolve `Connection reset by peer error`

# 1.7.3 (2022-03-14)
 - Loads `supermercado` on request because binaries for arm64 MacOS and Windows are not easily available.
 - Hide deprecated `add-source` command from command list.
 - Raise error in `tilesets status` for non-200s (includes unpublished tilesets).

# 1.7.2 (2021-10-01)
- Provide description for `upload-source` command, and label `add-source` command as deprecated.

# 1.7.1 (2021-04-16)
- Switch to codecov python module

# 1.7.0 (2021-04-02)
- Update `tilesets publish` success message to include link to studio.mapbox.com/tilesets/* endpoint and include `tilesets job` command to view the status.

# 1.6.0 (2021-02-16)
- Fix problem that prevented estimate-area from working for MultiPolygons
- Improve documentation for delete-source and upload-source

# 1.5.1 (2020-10-19)
- Update README for estimate-area

# 1.5.0 (2020-10-19)
- Create estimate-area command

# 1.4.3 (2020-10-08)
- Update Click version to 7.1.2 and fix assertions to pass all tests

# 1.4.2 (2020-08-18)
- Check if the token matches the username before uploading sources

# 1.4.1 (2020-08-06)
- Use the `/jobs` endpoint in the `status` command

# 1.4.0 (2020-08-04)
- Create upload-source command to replace add-source, with extra `--replace` option

# 1.3.0 (2020-07-30)
- Official PyPi release via TravisCI

# 1.2.1.dev0 (2020-07-24)
- Send compact JSON during source upload

# 1.2.0.dev0 (2020-07-16)
- Pin pytest version
- Add `--type`, `--visibility`, `--sortby`, and `--limit` options to `list` command
- Make TilesetNameError message more descriptive
- Fail early if no access_token is provided
- Add `--limit` option to `jobs` command
- Update `add-source` to show a progress bar
- Add `--quiet` option to `add-source` to silence progress bar

# 1.1.0.dev0 (2020-06-11)
- `update-recipe` command handles 204 status code in addition to 201 and no longer prints response text
- Add `update` command for updating `--name`, `--description`, `--privacy`, and `--attribution` of a tileset
- Add `--attribution` option to the `create` command
- Add `delete` command for deleting a tileset
- Add `tilejson` command
- Add user-agent header to API requests

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
