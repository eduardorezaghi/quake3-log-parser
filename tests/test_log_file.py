import pytest

from src.dclasses.quake_log import QuakeLog
from src.parser import QuakeLogParser


@pytest.fixture
def create_mock_log_file(tmp_path):
    def _create_file(content):
        file_path = tmp_path / "test.log"
        file_path.write_text(content)
        return file_path

    return _create_file


@pytest.mark.parametrize(
    "initial_state, command, expected_count, expected_state",
    [
        (False, "InitGame", 0, True),
        (True, "InitGame", 0, True),
        (False, "ShutdownGame", 0, False),
        (True, "ShutdownGame", 1, False),
    ],
)
def test_count_games(
    create_mock_log_file, initial_state, command, expected_count, expected_state
):
    log_content = f"0:00 {command}:\n"
    mock_file = create_mock_log_file(log_content)
    parser = QuakeLogParser(mock_file)
    parser._start_new_game() if initial_state else None

    parser._count_games(command)

    assert len(parser.games) == expected_count
    assert isinstance(parser.current_game, QuakeLog) == expected_state


@pytest.mark.parametrize(
    "log_content, expected_game_count, expected_final_state",
    [
        (
            """
    0:00 InitGame:
    15:00 ShutdownGame:
    """,
            1,
            False,
        ),
        (
            """
    0:00 InitGame:
    15:00 ShutdownGame:
    20:00 InitGame:
    """,
            1,
            True,
        ),
        (
            """
    0:00 InitGame:
    15:00 ShutdownGame:
    20:00 InitGame:
    25:00 ShutdownGame:
    """,
            2,
            False,
        ),
        (
            """
    0:00 InitGame:
    15:00 Exit: Timelimit hit.
    20:00 ShutdownGame:
    25:00 InitGame:
    30:00 Exit: Fraglimit hit.
    35:00 ShutdownGame:
    """,
            2,
            False,
        ),
        ("", 0, False),
    ],
)
def test_parse_log_file(
    create_mock_log_file, log_content, expected_game_count, expected_final_state
):
    mock_file = create_mock_log_file(log_content)
    parser = QuakeLogParser(mock_file)

    parser.parse()

    assert len(parser.games) == expected_game_count
    assert isinstance(parser.current_game, QuakeLog) == expected_final_state
