import pytest

from src.parser import QuakeLogParser


@pytest.mark.parametrize("content", ["This is some mock file content"])
def test_log_file_should_be_opened(mock_file):
    parser = QuakeLogParser(mock_file)

    content = None
    with parser.log_file as file:
        content = file.read()

    assert parser.log_file is not None
    assert parser.log_file.closed is True
    assert parser.log_file.name.endswith("test.log")
    assert content == "This is some mock file content"
