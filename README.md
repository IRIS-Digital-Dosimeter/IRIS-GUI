# IRIS-GUI
A Python CLI and GUI tool that allows easy updating, uploading, and access to the IRIS boards.

## Requirements:

- **uv**
    - https://docs.astral.sh/uv/
    - A package and project manager

- **Python 3.12+**
    - can/should install with `uv python install <version>`
    - see [this page](https://docs.astral.sh/uv/guides/install-python/) for more help



`uv` will download the necessary packages when you attempt to run any programs in the repo with `uv run [file]`.

## Usage

1. `cd` into the root directory of this repository

2. run `uv python install`

3. run `uv run textualtest.py`

## To Do

- [x] Fix bug where uploading says "Invalid Path" for all paths
- [x] Find a better way to get board details