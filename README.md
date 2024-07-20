# quake3-log-parser

This is a simple parser for Quake 3 Arena logs. It is written in Python and uses regular expressions to parse the logs.

```
quake3-log-parser/
├── src
├── tests
├── Dockerfile
├── README.md
├── TESTING.MD
├── poetry.lock
├── pyproject.toml
└── ruff.toml
```


## Author

- Eduardo Rezaghi - [Github](https://github.com/eduardorezaghi) | [LinkedIn](https://www.linkedin.com/in/eduardo-rezaghi/)

## Dependencies

- Python 3.11 or higher
- `poetry`
- `pytest`
- `pytest-cov`
- `pytest-mock`
- `pytest-xdist` _(for parallel testing)_
- `ruff`
- `ruff-lsp` 
- `tinydb`

## Usage (via Docker)

You can conveniently run the parser using Docker.
To do so, you must first build the image:

```bash
docker build -t quake3-log-parser .
```

Then, you can run the image with the following command:
```bash
docker run --rm --name quake3-log-parse -it quake3-log-parser
```
This will run the parser and remove the container once it finishes.


## Installation

First, you must ensure that you have Python 3.11 or higher installed on your machine. 
You can download it from the [official website](https://www.python.org/downloads/), 
or using a tool like [pyenv](https://github.com/pyenv/pyenv) or [asdf](https://asdf-vm.com/).

This project uses [poetry](https://python-poetry.org/) to manage dependencies.  
You can install it using `pipx`, `pip` or `brew`:

```bash
pipx install poetry
```
You can check if poetry was successfully installed by running `poetry --version`.

To install the dependencies, run the following command in the project's root directory:

```bash
poetry install
```
It will install all the dependencies listed in the `pyproject.toml` file. You can check the installed dependencies by running `poetry show`.

To activate the virtual environment, run:

```bash
poetry shell
```


## Running the parser
---
You can use python to run the CLI parser.
The most basic usage is to run the parser with the log file as an argument:

```bash
python -m src.main <path_to_log_file>
```

For example, running `python -m src.main ./qgames.log` will parse the `qgames.log` file, returning the parsed data.
