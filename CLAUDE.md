# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`mapbox-tilesets` is a CLI tool for interacting with the [Mapbox Tiling Service (MTS)](https://docs.mapbox.com/mapbox-tiling-service/overview/) API. It manages tilesets, sources, recipes, jobs, and changesets via REST API calls.

## Commands

This project uses `uv` as the package manager.

```bash
# Install dependencies
uv sync --group dev

# Install with optional area estimation support
uv sync --group dev --extra estimate-area

# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov --cov-config=.coveragerc --cov-report=term-missing

# Run a single test file
uv run pytest tests/test_cli_create.py

# Run a single test
uv run pytest tests/test_cli_create.py::test_create

# Lint and format (pre-commit runs ruff)
uv run pre-commit run --all-files

# Setup pre-commit hooks (once after cloning)
uv run pre-commit install
```

## Architecture

All CLI commands are defined in a single file: `mapbox_tilesets/scripts/cli.py`. This is intentional — the project is a focused API wrapper and the monolithic structure keeps everything discoverable.

**Request flow:**
```
Click command → utils._get_token() + utils._get_session() → HTTP request to Mapbox API → output to stdout
```

**Key files:**
- `mapbox_tilesets/scripts/cli.py` — All 25+ Click commands (create, publish, upload-source, validate-recipe, estimate-area, etc.)
- `mapbox_tilesets/utils.py` — Token/URL resolution, session setup, tileset ID validation, GeoJSON validation, area estimation
- `mapbox_tilesets/errors.py` — `TilesetsError` and `TilesetNameError` (both extend `click.ClickException`)

**Authentication:** Mapbox access tokens are read from the `MAPBOX_ACCESS_TOKEN` environment variable or the `--token` CLI flag.

**Test fixtures:** `tests/fixtures/` contains GeoJSON files and recipes used across tests. `tests/conftest.py` provides shared fixtures including `MockResponse` and token environment setup.

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit and merge to master
4. Tag: `git tag -a v{version} -m 'v{version}' && git push --tags`
5. GitHub Actions publishes to PyPI automatically
