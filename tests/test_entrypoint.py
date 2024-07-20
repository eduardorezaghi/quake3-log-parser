import argparse
import json
from unittest.mock import patch

import pytest

from src.dclasses import QuakeLogEncoder
from src.main import parse_arguments, run
from src.parser import QuakeLogParser

SAMPLE_LOG_CONTENT = """
------------------------------------------------------------
InitGame: 
------------------------------------------------------------
"""


# Tests
def test_parse_arguments():
    # Test valid arguments
    with patch("sys.argv", ["main.py", "sample.log", "--group-deaths"]):
        args = parse_arguments()
        assert args.log_file == "sample.log"
        assert args.group_deaths is True

    # Test missing arguments
    with patch("sys.argv", ["main.py"]):
        with pytest.raises(SystemExit):  # argparse raises SystemExit on error
            parse_arguments()


def test_run_valid_file(create_mock_log_file):
    log_file = create_mock_log_file(SAMPLE_LOG_CONTENT)
    with patch("argparse.ArgumentParser.parse_args") as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            log_file=str(log_file), group_deaths=False
        )
        with patch("builtins.print") as mock_print:
            run(mock_parse_args.return_value)
            mock_print.assert_called_once_with(
                json.dumps(
                    QuakeLogParser(log_file).games, indent=4, cls=QuakeLogEncoder
                )
            )


def test_run_valid_file_with_group_deaths(create_mock_log_file):
    log_file = create_mock_log_file(SAMPLE_LOG_CONTENT)
    with patch("argparse.ArgumentParser.parse_args") as mock_parse_args:
        mock_parse_args.return_value = argparse.Namespace(
            log_file=str(log_file), group_deaths=True
        )
        with patch("builtins.print") as mock_print:
            run(mock_parse_args.return_value)
            mock_print.assert_called_once_with(
                json.dumps(
                    QuakeLogParser(log_file)._group_deaths_by_means(),
                    indent=4,
                    cls=QuakeLogEncoder,
                )
            )


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(log_file="non_existent.log"),
)
@patch("src.main.Path.is_file", return_value=False)
def test_run_with_nonexistent_file(mock_is_file, mock_parse_args):
    with pytest.raises(FileNotFoundError) as e:
        run(argparse.Namespace(log_file="non_existent.log"))
    assert str(e.value) == "Error: The file non_existent.log does not exist."
