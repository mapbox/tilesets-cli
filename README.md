# tilesets-cli

[![Build Status](https://travis-ci.com/mapbox/tilesets-cli.svg?token=wqR3RcWUEprcQ1ttsgiP&branch=master)](https://travis-ci.com/mapbox/tilesets-cli) [![codecov](https://codecov.io/gh/mapbox/tilesets-cli/branch/master/graph/badge.svg?token=YBTKyc2o3j)](https://codecov.io/gh/mapbox/tilesets-cli)

CLI for interacting with and preparing data for the [Mapbox Tiling Service](https://docs.mapbox.com/mapbox-tiling-service/overview/).

📚 If you have a question that isn't answered here, please refer to the complete [Mapbox Tiling Service documentation](https://docs.mapbox.com/mapbox-tiling-service/overview/).

# Contributing

[CONTRIBUTING.md](/CONTRIBUTING.md) includes information about release processes & running tests. :raised_hands:

# Installation

## Requirements

- Python >= 3.6 (can be installed via virtualenv)
- Recommended: [virtualenv](https://virtualenv.pypa.io/) / [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

## Basic installation

`pip install mapbox-tilesets` will install everything but [`estimate-area`](#estimate-area).

## Installing optional `estimate-area` command

If you are using an x86 Mac or Linux machine, run:
`pip install 'mapbox-tilesets[estimate-area]'`

Otherwise, you will need to install some dependencies.

### arm64 MacOS

If you're on an arm64 Mac (e.g., with an M1 chip), you'll need to install [GDAL](https://gdal.org/) first. On Mac, a simple way is to use [Homebrew](https://brew.sh/):

```sh
$ brew install gdal
...
$ pip install 'mapbox-tilesets[estimate-area]'
```

### Windows

Note, Windows is not officially supported at this time.

Windows users need to install [GDAL](http://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal) and [rasterio](http://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio).
Then `pip install 'mapbox-tilesets[estimate-area]'`

## Installing optional `estimate-cu` command

If you are using an x86 Mac or Linux machine, run:
`pip install 'mapbox-tilesets[estimate-cu]'`

Otherwise, you will need to install some dependencies.

### arm64 MacOS

If you're on an arm64 Mac (e.g., with an M1 chip), you'll need to install [GDAL](https://gdal.org/) first. On Mac, a simple way is to use [Homebrew](https://brew.sh/):

```sh
$ brew install gdal
...
$ pip install 'mapbox-tilesets[estimate-cu]'
```

### Windows

Note, Windows is not officially supported at this time.

Windows users need to install [GDAL](http://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal) and [rasterio](http://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio).
Then `pip install 'mapbox-tilesets[estimate-cu]'`

## Mapbox Access Tokens

In order to use the tilesets endpoints, you need a Mapbox Access Token with `tilesets:write`, `tilesets:read`, and `tilesets:list` scopes. This is a secret token, so do not share it publicly!

You can either pass the Mapbox access token to each command with the `--token` flag or export it as an environment variable. Acceptable values are:

- `MAPBOX_ACCESS_TOKEN`
- `MapboxAccessToken`

Set the environment variable with `export`

```
export MAPBOX_ACCESS_TOKEN=my.token
```

# Commands

- Tileset Sources
  - [`upload-source`](#upload-source)
  - [`upload-raster-source`](#upload-raster-source) (new)
  - _deprecated_ [`add-source`](#deprecated-add-source)
  - [`validate-source`](#validate-source)
  - [`view-source`](#view-source)
  - [`list-sources`](#list-sources)
  - [`delete-source`](#delete-source)
  - [`estimate-area`](#estimate-area)
  - [`estimate-cu`](#estimate-cu)
- Recipes
  - [`view-recipe`](#view-recipe)
  - [`validate-recipe`](#validate-recipe)
  - [`update-recipe`](#update-recipe)
- Tilesets
  - [`create`](#create)
  - [`publish`](#publish)
  - [`update`](#update)
  - [`delete`](#delete)
  - [`status`](#status)
  - [`job`](#job)
  - [`jobs`](#jobs)
  - [`list`](#list)
  - [`tilejson`](#tilejson)
- Activity
  - [`list-activity`](#list-activity)

### upload-source

```shell
tilesets upload-source <username> <source_id> <file>
```

Uploads GeoJSON files to a source for tiling. Accepts line-delimited GeoJSON or GeoJSON feature collections as files or via `stdin`. The CLI automatically converts data to line-delimited GeoJSON prior to uploading. Can be used to add data to a source or to replace all of the data in a source with the `--replace` flag.

Please note that if your source data is a FeatureCollection, `tilesets` must read it all into memory to split it up into separate features before uploading it to the Tilesets API. You are strongly encouraged to provide your data in line-delimited GeoJSON format instead, especially if it is large.

Note: for large file uploads that are taking a very long time, try using the `--no-validation` flag.

Flags:

- `--no-validation` [optional]: do not validate source data locally before uploading, can be helpful for large file uploads
- `--replace` [optional]: delete all existing source data and replace with data from the file
- `--quiet` [optional]: do not display an upload progress bar

Usage

```shell
# single file
tilesets upload-source <username> <source_id> ./file.geojson

# multiple files
tilesets upload-source <username> <source_id> file-1.geojson file-4.geojson

# directory of files
# Reading from a directory will not distinguish between GeoJSON files and non GeoJSON files. All source files will be run through our validator unless you pass the `--no-validation` flag.
tilesets upload-source <username> <source_id> ./path/to/multiple/files/
```
### upload-raster-source

```shell
tilesets upload-raster-source <username> <source_id> <file>
```

Uploads Raster files to a source for tiling. Accepts GeoTIFF, NetCDF and GRIB formats right now. Can be used to add data to a source or to replace all of the data in a source with the `--replace` flag.

Learn more about the supported formats and using Raster source [here](https://docs.mapbox.com/mapbox-tiling-service/guides/).

Flags:

- `--replace` [optional]: delete all existing source data and replace with data from the file
- `--quiet` [optional]: do not display an upload progress bar

Usage

```shell
# single file
tilesets upload-raster-source <username> <source_id> ./file.tif

# multiple files
tilesets upload-raster-source <username> <source_id> file-1.tif file-4.tif
```

### _deprecated_ add-source

_WARNING: add-source is maintained for legacy purposes. Please use the `upload-source` command instead._

```shell
tilesets add-source <username> <source_id> <file>
```

Adds GeoJSON files to a source for tiling. Accepts line-delimited GeoJSON or GeoJSON feature collections as files or via `stdin`. The CLI automatically converts data to line-delimited GeoJSON prior to uploading.

Please note that if your source data is a FeatureCollection, `tilesets` must read it all into memory to split it up into separate features before uploading it to the Tilesets API. You are strongly encouraged to provide your data in line-delimited GeoJSON format instead, especially if it is large.

Flags:

- `--no-validation` [optional]: do not validate source data locally before uploading
- `--quiet` [optional]: do not display an upload progress bar

Usage

```shell
# single file
tilesets add-source <username> <source_id> ./file.geojson

# multiple files
tilesets add-source <username> <source_id> file-1.geojson file-4.geojson

# directory of files
# Reading from a directory will not distinguish between GeoJSON files and non GeoJSON files. All source files will be run through our validator unless you pass the `--no-validation` flag.
tilesets add-source <username> <source_id> ./path/to/multiple/files/
```

### validate-source

```shell
tilesets validate-source <path>
```

Validates a line delimited GeoJSON source file locally. Example error output:

```JSON
Invalid line delimited geojson.
```

### view-source

```
tilesets view-source <username> <source_id>
```

Get information for a tileset source, such as number of files, the size in bytes, and the ID in mapbox:// protocol format.

### list-sources

```
tilesets list-sources <username>
```

List all tileset sources from a particular account. Response is an array of sources.

### delete-source

```
tilesets delete-source <username> <source_id>
```

Permanently delete a tileset source and all of its files. This is not a recoverable action!

Flags:

- `-f` or `--force`: Do not ask for confirmation before deleting

Usage

```shell
# to delete mapbox://tileset-source/user/source_id
tilesets delete-source user source_id
```

### estimate-cu

```shell
tilesets estimate-cu <tileset> -s/--sources <sources> -b/--num-bands <number> --raw
```

Estimates the CU value of a tileset before publishing it. This is useful to understand the estimated cost a given tileset before you start processing the data. Note: This is currently only available to tileset recipes with type `raster` or `rasterarray`.

See https://docs.mapbox.com/help/glossary/compute-unit/ for more information.

Flags:
- `-s` or `--sources` [optional]: Local path to the sources that your recipe points at. This is highly recommeneded.
- `-b` or `--num-bands` [optional]: The number of bands you expect your recipe to select across all layers. This is recommended.
- `--minzoom` [optional]: Use this flag if your recipe does not contain a minzoom value.
- `--maxzoom` [optional]: Use this flag if your recipe does not contain a maxzoom value.
- `--raw` [optional]: This will toggle the pretty print output.

Usage

```shell
# Estimate the CUs for 'account.tileset' with sources located in 'path/to/sources/' and a band count of 20.
tilesets estimate-cu account.tileset -s 'path/to/sources/*.grib2' -b 20

# Estimate the CUs for 'account.tileset' for a single source and a band count of 10 (pretty print the results)
tilesets estimate-cu account.tileset -s 'path/to/sources/helloworld.grib2' -b 10 --raw
```

### estimate-area

```shell
tilesets estimate-area <features> -p/--precision <precision>
```

Estimates tiled area (km<sup>2</sup>) of features with a specified precision. Accepts line-delimited GeoJSON or GeoJSON feature collections as files or via `stdin` or a list of string-encoded coordinate pairs of the form "[lng, lat]", or "lng, lat", or "lng lat". Precision must be 10m, 1m, 30cm or 1cm.

Flags:

- `-p` or `--precision` [required]: precision level
- `--no-validation` [optional]: do not validate source data locally before area calculation
- `--force-1cm` [optional]: the --force-1cm flag must be present to enable 1cm precision area calculation and may take longer for large feature inputs or data with global extents. 1cm precision for tileset processing is only available upon request after contacting [Mapbox support](https://support.mapbox.com/hc/en-us/requests/new?ticket_form_id=360000291231)

Usage

```shell

# GeoJSON feature files
tilesets estimate-area ./file1.geojson ./file2.geojson -p <precision>

# GeoJSON features in stdin redirection 1
tilesets estimate-area -p <precision> < ./file.geojson

# GeoJSON features in stdin redirection 2
cat ./file.geojson | tilesets estimate-area -p <precision>

# GeoJSON features in stdin stream
tilesets estimate-area --precision <precision>
<features>

# coordinate pairs (must be in quotes)
tilesets estimate-area "[lng,lat]" "[lng,lat]" --precision <precision>
```

### view-recipe

Prints the Recipe JSON to stdout.

```shell
tilesets view-recipe <tileset_id>
```

### validate-recipe

Validates a Recipe JSON document.

```shell
tilesets validate-recipe /path/to/recipe.json
```

Example `recipe.json`:

```
{
  "version": 1,
  "layers": {
    "trees": {
      "source": "mapbox://tileset-source/{username}/trees-data",
      "minzoom": 4,
      "maxzoom": 8
    }
  }
}
```

See more details about the recipe spec [here](https://docs.mapbox.com/help/troubleshooting/tileset-recipe-reference).
See recipe examples [here](https://docs.mapbox.com/help/troubleshooting/tileset-recipe-examples).

Example error output:

```JSON
{
  "errors": [
    "Unknown top-level key \"potato\"."
  ],
  "valid": false
}
```

### update-recipe

Update the Recipe JSON for a tileset. Performs a server-side validation of the new document.

This command only supports tilesets created with the [Mapbox Tiling Service](https://docs.mapbox.com/mapbox-tiling-service/overview/).

```shell
tilesets update-recipe <tileset_id> /path/to/recipe.json
```

### create

Creates a brand new, empty tileset with a recipe passed in from your local filesystem.

```shell
tilesets create <tileset_id> --recipe /path/to/recipe.json --name "My neat tileset"
```

The `tileset_id` is in the form of `username.handle` - for example "mapbox.neat-tileset". The handle may only include "-" or "\_" special characters and must be 32 characters or fewer.

Flags:

- `--recipe` or `-r` [required]: path to your Recipe JSON document
- `--name` or `-n` [required]: human-readable name of your tileset. (If your tileset_id is user.my_amazing_tileset, you might want your `name` field to be "My Amazing Tileset".)
- `--description` or `-d`: description of your tileset
- `--privacy` or `-p`: Set the privacy of the tileset. Allowed values are `private` and `public`. By default, new tilesets are private.
- `--attribution` or `-a` [optional]: set tileset attribution. Must be a JSON string, specifically an array of attribution objects, each with `text` and `link` keys. Limited to three attribution objects, 80 characters maximum combined across all text values, and 1000 characters maximum combined across all link values.

### publish

Queues a tiling _job_ using the recipe provided. Use to publish a new tileset or update an existing one. Returns a job ID for progress tracking.

This command only supports tilesets created with the [Mapbox Tiling Service](https://docs.mapbox.com/mapbox-tiling-service/overview/).

```
tilesets publish <tileset_id>
```

### update

Update a tileset's information.

```
tilesets update <tileset_id>
  --name "Hello World"
  --description "Say hi to the world"
  --privacy=private
  --attribution='[{"text":"© Hola Mundo","link":"http://example.com"}]'
```

Flags:

- `--name` or `-n` [optional]: update tileset name
- `--description` or `-d` [optional]: update tileset description
- `--privacy` or `-p` [optional]: set your tileset to `public` or `private`
- `--attribution` or `-a` [optional]: set tileset attribution. Must be a JSON string, specifically an array of attribution objects, each with `text` and `link` keys. Limited to three attribution objects, 80 characters maximum combined across all text values, and 1000 characters maximum combined across all link values.

### delete

Delete a tileset. By default will prompt you for confirmation before deleting.

```
tilesets delete <tileset_id>
```

Flags:

- `--force` or `-f` to bypass confirmation prompt.

### status

View the status of the most recent job for a tileset. To get more detailed information about a tileset's jobs, including the timestamps of failed and successful jobs, use the `tilesets jobs <tileset_id>` command.

```
tilesets status <tileset_id>
```

### job

Retrieve a single job for a tileset.

This command only supports tilesets created with the [Mapbox Tiling Service](https://docs.mapbox.com/mapbox-tiling-service/overview/).

```shell
tilesets job <tileset_id> <job_id>
```

**What is a job?** Each time you generate or regenerate your output tileset via the `publish` command (whether that's a new recipe or new source data), a single job is created that processes your data. A tileset can have many jobs, each with a unique identifier. When you publish a tileset, the HTTP response includes the unique job identifier that corresponds to the most recent job. To read more about HTTP design, see this [documentation](https://docs.mapbox.com/api/maps/#tilesets).

### jobs

Check all jobs associated with a tileset. You can filter jobs by a particular `stage` - processing, queued, success, or failed.

This command only supports tilesets created with the [Mapbox Tiling Service](https://docs.mapbox.com/mapbox-tiling-service/overview/).

```shell
tilesets jobs <tileset_id> --stage=processing
```

Flags:

- `--stage` [optional]: filter by the stage of jobs
- `--limit [1-500]` [optional]: the maximum number of results to return, from 1 to 500. The default is 100.

### list

List all tilesets for an account. Just lists tileset IDs by default. Use the `--verbose` option for more information.

```shell
tilesets list <username>
```

Flags:

- `--type [vector|raster|rasterarray]` [optional]: filter results by tileset type
- `--visibility [public|private]` [optional]: filter results by visibility
- `--sortby [created|modified]` [optional]: sort results by their `created` or `modified` timestamps
- `--limit [1-500]` [optional]: the maximum number of results to return, from 1 to 500. The default is 100.
- `--verbose` [optional]: will list out the entire response object from the API

### tilejson

View the TileJSON for a tileset. `tileset_id` can be a comma-separated list of up to 15 tilesets for composited requests.

A TileJSON document, according to the [specification](https://github.com/mapbox/tilejson-spec), attempts to create a standard for representing metadata about multiple types of web-based layers, to aid clients in configuration and browsing.

```
tilesets tilejson <tileset_id>
```

Flags:

- `--secure`: By default, resource URLs in the retrieved TileJSON (such as in the "tiles" array) will use the HTTP scheme. Include this query parameter in your request to receive HTTPS resource URLs instead.

### list-activity

Lists total request counts for a user's tilesets in the past 30 days. Returns a pagination key `next` if there are more results than the return limit that can be passed into another command as the `start` argument.

```shell
tilesets list-activity <account>
```

Flags:

- `--sortby [requests|modified]` [optional]: Sorting key (default: requests)
- `--orderby [asc|desc]` [optional]: Ordering key (default: desc)
- `--limit [1-500]` [optional]: The maximum number of results to return (default: 100)
- `--indent` [optional]: Indent size for JSON output.
- `--start` [optional]: Pagination key from the `next` value in a response that has more results than the limit.
