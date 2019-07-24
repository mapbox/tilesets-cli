# tilesets-cli

[![Build Status](https://travis-ci.com/mapbox/tilesets-cli.svg?token=wqR3RcWUEprcQ1ttsgiP&branch=master)](https://travis-ci.com/mapbox/tilesets-cli) [![codecov](https://codecov.io/gh/mapbox/tilesets-cli/branch/master/graph/badge.svg?token=YBTKyc2o3j)](https://codecov.io/gh/mapbox/tilesets-cli)

CLI for interacting with and preparing data for the Mapbox Tilesets API.

## Requirements
- (optional) [virtualenv](https://virtualenv.pypa.io/)
- Python >= 3.6 (can be installed via virtualenv)

## Installation

```shell
# clone
git clone git@github.com:mapbox/tilesets-cli.git
cd tilesets-cli

# virtual env (optional)
mkvirtualenv tilesets-cli

# install deps
pip install .

# confirm installation was successful
tilesets --help
tilesets --version
```

## Access Tokens

In order to use the tilesets endpoints, you need a Mapbox Access Token with `tilesets:write` and `tilesets:read` scopes. This is a secret token, so do not share it publicly!

You can either pass the Mapbox access token to each command with the `--token` flag or export it as an environment variable. Acceptable values are:

* `MAPBOX_ACCESS_TOKEN`
* `MapboxAccessToken`

Set the environment variable with `export`
```
export MAPBOX_ACCESS_TOKEN=my.token
```

## Commands

### create

Creates a brand new, empty tileset with a recipe passed in from your local filesystem.

```shell
tilesets create <tileset_id> --recipe /path/to/recipe.json --name "My neat tileset"
```

Flags:

* `--recipe` or `-r` [required]: path to your Recipe JSON document
* `--name` or `-n` [required]: human-readable name of your tileset. (If your tileset_id is user.my_amazing_tileset, you might want your `name` field to be "My Amazing Tileset".)
* `--description` or `-d`: description of your tileset
* `--privacy` or `-p`: Set the privacy of the tileset. Allowed values are `private` and `public`. If not provided, will default to your plan level on Mapbox.com. Pay-As-You-Go plans only support public maps.
* `--token` or `-t`: The Mapbox access token. If not provided, a `MAPBOX_ACCESS_TOKEN` or `MapboxAccessToken` environment variable is required.

### upload

Upload a file or set of files to a tileset's staging area.

```shell
# single file
tilesets upload <tileset_id> ./file.geojson

# multiple files
tilesets upload <tileset_id> file-1.geojson file-4.geojson

# directory of files
tilesets upload <tileset_id> ./my-data
```

Flags:

* `--token` or `-t`: The Mapbox access token. If not provided, a `MAPBOX_ACCESS_TOKEN` or `MapboxAccessToken` environment variable is required.

*Note*
- Reading from a directory will not distinguish between GeoJSON files and non GeoJSON files.
- All source files will be run through our validator unless you pass the `--no-validation` flag.

### publish

Kicks off a tiling process with all of the batch files in the staging area.

```
tilesets publish <tileset_id>
```

Flags:

* `--token` or `-t`: The Mapbox access token. If not provided, a `MAPBOX_ACCESS_TOKEN` or `MapboxAccessToken` environment variable is required.

### status

View the status of a tileset. This includes how many publish jobs are queued, processing, and complete.

```
tilesets status <tileset_id>
```

Flags:

* `--token` or `-t`: The Mapbox access token. If not provided, a `MAPBOX_ACCESS_TOKEN` or `MapboxAccessToken` environment variable is required.

### validate-source

Validates a line delimited GeoJSON source file.

```
tilesets validate-source path/to/source/file
```

Example error output:

```JSON
Invalid line delimited geojson.
```

### validate-recipe

Validates a Recipe JSON document.

```shell
tilesets validate-recipe /path/to/recipe.json
```

Flags:

* `--token` or `-t`: The Mapbox access token. If not provided, a `MAPBOX_ACCESS_TOKEN` or `MapboxAccessToken` environment variable is required.

Example `recipe.json`:
```
{
  "minzoom": 9,
  "maxzoom": 16,
  "layer_name": "states"
}
```
See more details about the recipe spec [here](https://docs.google.com/document/d/1GA2QLmxX6b6rMoOKVHbg1EOd6miLOhD28DyOWf361d0/edit#heading=h.2zs0vdp63wzk).
See recipe examples [here](https://docs.google.com/document/d/1Vs1F5rGRu-VwTULrL0Ie6EKNq9r_eIf0LFOujYKRbEY/edit).

Example error output:

```JSON
{
  "errors": [
    "Unknown top-level key \"potato\"."
  ],
  "valid": false
}
```

### view-recipe

Prints the Recipe JSON to stdout.

```shell
tilesets view-recipe <tileset_id>
```

Flags:

* `--token` or `-t`: The Mapbox access token. If not provided, a `MAPBOX_ACCESS_TOKEN` or `MapboxAccessToken` environment variable is required.

### update-recipe

Update the Recipe JSON for a tileset. Performs a server-side validation of the new document.

```shell
tilesets update-recipe <tileset_id> /path/to/recipe.json
```

### View Jobs*

Check all jobs associated with a tileset. You can filter jobs by a particular `stage` - processing, queued, success, or failed.


```shell
tilesets jobs <tileset_id> --stage=processing
```
Flags:

- --token or -t: The Mapbox access token. If not provided, a MAPBOX_ACCESS_TOKEN or MapboxAccessToken environment variable is required.
- --stage: Filter by the stage of jobs. (Optional.)

### Retrieve a Single Job*

Retrieve a single job associated with a tileset based on a unique job id.

```shell
tilesets job <tileset_id> <job_id>
```

Flags:

- --token or -t: The Mapbox access token. If not provided, a MAPBOX_ACCESS_TOKEN or MapboxAccessToken environment variable is required.


*_What is a job? Each time you generate or regenerate your output tileset via the `publish` command (whether that's a new recipe or new source data), a single job is created that processes your data. A tileset can have many jobs, each with a unique identifier. When you publish a tileset, the HTTP response includes the unique job identifier that corresponds to the most recent job. To read more about HTTP design, see this (documentation)[https://docs.google.com/document/d/1Ys4-PmKRN3Bjdh2qux9eLUtT9PJ2MUQKadt_4188Xzc/edit#]._



## Contributing

[CONTRIBUTING.md](/CONTRIBUTING.md) includes information about release processes & running tests. :raised_hands:
