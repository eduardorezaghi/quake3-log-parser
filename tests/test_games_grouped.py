import pytest

from src.parser import QuakeLogParser
from src.dclasses import QuakeLog

@pytest.fixture
def create_mock_log_file(tmp_path):
    def _create_file(content):
        file_path = tmp_path / "test.log"
        file_path.write_text(content)
        return file_path

    return _create_file


@pytest.fixture(
    params=[
        ("tests/fixtures/qlog_shard_1.log", 5),
        ("tests/fixtures/qlog_shard_2.log", 4),
        ("tests/fixtures/qlog_shard_3.log", 4),
    ]
)
# For each test file, we expect a different number of games
def log_file_fixture(request):
    file_path, expected_game_count = request.param
    with open(file_path, "r") as f:
        content = f.read()
    return content, expected_game_count


def test_parse_games_grouped(create_mock_log_file, log_file_fixture):
    # Arrange
    log_content, expected_game_count = log_file_fixture
    mock_file = create_mock_log_file(log_content)
    log_parser = QuakeLogParser(mock_file)
    log_parser.parse()

    # Act
    parsed_games = log_parser._group_game_results()

    # Assert
    assert len(parsed_games) == expected_game_count
    assert len(log_parser.games) == expected_game_count
    # For each game in the parsed games, verify that the format is correct
    assert all(isinstance(game, QuakeLog) for game in log_parser.games)
