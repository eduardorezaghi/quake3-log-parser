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
## Table of Contents
1. [Author](#author)
2. [Dependencies](#dependencies)
3. [Usage (via Docker)](#usage-via-docker)
4. [Installation](#installation)
5. [Running the parser](#running-the-parser)
    1. [Summarized game information](#summarized-game-information)
    2. [Summarized grouped kills by game information](#summarized-grouped-kills-by-game-information)
6. [Running the tests](#running-the-tests)



## Author

- Eduardo Rezaghi - [Github](https://github.com/eduardorezaghi) | [LinkedIn](https://www.linkedin.com/in/eduardo-rezaghi/)

## Dependencies

- Python 3.12 or higher
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

Then, you can run the image with the following command.  
Make sure you replace `./logs/qgames.log` with the path to the log file you want to parse.
Example (assuming you are in the project's root directory):
```bash
docker run --rm --name "quake3-log-parser" -v $(pwd):/app/logs -it quake3-log-parser ./qgames.log
```
This will run the parser and remove the container once it finishes.


## Installation

First, you must ensure that you have Python 3.12 or higher installed on your machine. 
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
You can use python to run the CLI parser.
The most basic usage is to run the parser with the log file as an argument:

```bash
python -m src.main /path/to/logfile.log
```
For example, running `python -m src.main ./qgames.log` will parse the `qgames.log` file, returning the parsed data.  
The available output formats are as follows.

### Summarized game information
`python -m src.main ./logs/qgames.log`

```json
[
  {
    "game_1": {
      "total_kills": 0,
      "players": [
        "Isgalamido"
      ],
      "kills": {}
    }
  },
  {
    "game_2": {
      "total_kills": 9,
      "players": [
        "Isgalamido",
        "Mocinha",
        "Dono da Bola"
      ],
      "kills": {
        "Mocinha": -1,
        "Isgalamido": -7
      }
    }
  },
  {
    "game_3": {
      "total_kills": 4,
      "players": [
        "Isgalamido",
        "Zeh",
        "Mocinha",
        "Dono da Bola"
      ],
      "kills": {
        "Isgalamido": 1,
        "Mocinha": -1,
        "Dono da Bola": -1,
        "Zeh": -2
      }
    }
  },
  ...
]
```

### Summarized grouped kills by game information
`python -m src.main ./logs/qgames.log --group-deaths`
```json
[
  {
    "game_1": {
      "kills_by_means": {}
    }
  },
  {
    "game_2": {
      "kills_by_means": {
        "MOD_TRIGGER_HURT": 7,
        "MOD_ROCKET_SPLASH": 1,
        "MOD_FALLING": 1
      }
    }
  },
  {
    "game_3": {
      "kills_by_means": {
        "MOD_TRIGGER_HURT": 2,
        "MOD_ROCKET": 1,
        "MOD_FALLING": 1
      }
    }
  },
  ...
]
```

# Running the tests
See [TESTING.MD](./TESTING.MD) for instructions on how to run the tests.