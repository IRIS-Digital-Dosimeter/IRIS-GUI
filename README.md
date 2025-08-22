# IRIS-GUI
A Python CLI and GUI tool that allows easy updating, uploading, and access to the IRIS boards.

## Requirements:

- **uv**
    - https://docs.astral.sh/uv/
    - A package and project manager

- **Python 3.12+**
    - can install with `uv python install <version>`
    - see [this page](https://docs.astral.sh/uv/guides/install-python/) for more help

- **Tkinter**
    - check by running `uv run -m tkinter` in terminal of choice


`uv` will download the necessary packages when you attempt to run any programs in the repo with `uv run [file]`.

## To Do

- [] Fix bug where uploading says "Invalid Path" for all paths
- [] Find a better way to get board details