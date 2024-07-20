import argparse
from unittest.mock import patch

import pytest

from src.main import run


@patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(log_file="non_existent.log"),
)
@patch("src.main.Path.is_file", return_value=False)
def test_run_with_nonexistent_file(mock_is_file, mock_parse_args):
    with pytest.raises(FileNotFoundError) as e:
        run(argparse.Namespace(log_file="non_existent.log"))
    assert str(e.value) == "Error: The file non_existent.log does not exist."
