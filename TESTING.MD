# quake3-log-parser - testing

This document describes how to run the tests for the `quake3-log-parser` project.
It uses the following tools:

- pytest plugins:
  - `pytest-mock`
  - `pytest-xdist`
  - `pytest-cov`

The tests are located inside the `tests` directory.


## Coverage
The project uses the `pytest-cov` plugin to generate the coverage report.  
The default configuration already includes the coverage report.  

[pyproject.toml, line 26](./pyproject.toml#L26)
```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -v --numprocesses=4 --cov=src --cov-report=term-missing --cov-report=html:coverage_html_report"
...
```
Example of the coverage report:
```txt
---------- coverage: platform linux, python 3.12.4-final-0 -----------
Name                        Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------
src/dclasses/quake_log.py      13      0      6      0   100%
src/enums/enums.py             30      0      0      0   100%
src/main.py                    16      6      2      1    61%   8-10, 18-20
src/parser/base_parser.py       6      2      0      0    67%   17-18
src/parser/log_parser.py       53      0     20      1    99%   79->exit
-----------------------------------------------------------------------
TOTAL                         118      8     28      2    93%
Coverage HTML written to dir coverage_html_report
```


## Running the tests
To run the tests, install the project dependencies, as described in the [Installation](./README.md#installation) section.

Then, you can run the tests using the following command:

```
pytest
```

## Running the tests (via Docker)
To run the tests using Docker, you can use the following command:

```
docker run --rm --name "quake3-log-parser" -it quake3-log-parser pytest
```