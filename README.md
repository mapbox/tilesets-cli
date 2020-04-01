# tilesets-cli

[![Build Status](https://travis-ci.com/mapbox/tilesets-cli.svg?token=wqR3RcWUEprcQ1ttsgiP&branch=master)](https://travis-ci.com/mapbox/tilesets-cli) [![codecov](https://codecov.io/gh/mapbox/tilesets-cli/branch/master/graph/badge.svg?token=YBTKyc2o3j)](https://codecov.io/gh/mapbox/tilesets-cli)

CLI for interacting with and preparing data for [Mapbox Tilesets API](https://docs.mapbox.com/api/maps/#tilesets).

# Contributing

[CONTRIBUTING.md](/CONTRIBUTING.md) includes information about release processes & running tests. :raised_hands:

# Installation
`pip install mapbox-tilesets`

#### Requirements

- Python >= 3.6 (can be installed via virtualenv)
- Recommended: [virtualenv](https://virtualenv.pypa.io/) / [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

#### Mapbox Access Tokens

In order to use the tilesets endpoints, you need a Mapbox Access Token with `tilesets:write` and `tilesets:read` scopes. This is a secret token, so do not share it publicly!

You can either pass the Mapbox access token to each command with the `--token` flag or export it as an environment variable. Acceptable values are:

* `MAPBOX_ACCESS_TOKEN`
* `MapboxAccessToken`

Set the environment variable with `export`
```
export MAPBOX_ACCESS_TOKEN=my.token
```

# Commands

* Tileset Sources
  * [`add-source`](#add-source)
  * [`validate-source`](#validate-source)
  * [`view-source`](#view-source)
  * [`list-sources`](#list-source)
  * [`delete-source`](#delete-source)
* Recipes
  * [`view-recipe`](#view-recipe)
  * [`validate-recipe`](#validate-recipe)
  * [`update-recipe`](#update-recipe)
* Tilesets
  * [`create`](#create)
  * [`publish`](#publish)
  * [`status`](#status)
  * [`job`](#job)
  * [`jobs`](#jobs)
  * [`list`](#list)

### add-source

```shell
tilesets add-source <username> <id> <file>
```

Flags:

* `--no-validation` [optional]: do not validate source data locally before uploading

Usage

```shell
# single file
tilesets add-source <username> <id> ./file.geojson

# multiple files
tilesets add-source <username> <id> file-1.geojson file-4.geojson

# directory of files
tilesets add-source <username> <id> ./path/to/multiple/files/
```

Reading from a directory will not distinguish between GeoJSON files and non GeoJSON files. All source files will be run through our validator unless you pass the `--no-validation` flag.

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
tilesets view-source <username> <id>
```

Get information for a tileset source, such as number of files, the size in bytes, and the ID in mapbox:// protocol format.

### list-sources

```
tilesets list-sources <username>
```

List all tileset sources from a particular account. Response is an array of sources.

### delete-source

```
tilesets delete-source
```

Permanently delete a tileset source and all of its files. This is not a recoverable action!

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

```shell
tilesets update-recipe <tileset_id> /path/to/recipe.json
```

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

### publish

Queues a tiling _job_ using the recipe provided. Use to publish a new tileset or update an existing one. Returns a job ID for progress tracking.

```
tilesets publish <tileset_id>
```

### status

View the status of a tileset. This includes how many jobs are queued, processing, and complete.

```
tilesets status <tileset_id>
```

### job

Retrieve a single job for a tileset.

```shell
tilesets job <tileset_id> <job_id>
```

**What is a job?** Each time you generate or regenerate your output tileset via the `publish` command (whether that's a new recipe or new source data), a single job is created that processes your data. A tileset can have many jobs, each with a unique identifier. When you publish a tileset, the HTTP response includes the unique job identifier that corresponds to the most recent job. To read more about HTTP design, see this [documentation](https://docs.mapbox.com/api/maps/#tilesets).

### jobs

Check all jobs associated with a tileset. You can filter jobs by a particular `stage` - processing, queued, success, or failed.


```shell
tilesets jobs <tileset_id> --stage=processing
```

- --stage: Filter by the stage of jobs. (Optional.)

### list

List all tilesets for an account. Just lists tileset IDs by default. Use the `--verbose` option for more information.

```shell
tilesets list <username>
```

- --verbose: will list out the entire response object from the API
