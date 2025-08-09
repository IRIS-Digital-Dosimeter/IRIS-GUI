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


In order to download required packages, please run the following in a terminal:
`pip -R install ./requirements.txt`

If you're using Linux and have issues using `pip` for Python packages, you may have to use your package manager to manually install them. The list of dependencies can be found in `./requirements.txt`.






# To Do
- [] Fix bug where uploading says "Invalid Path" for all paths
- [] Find a better way to get board details