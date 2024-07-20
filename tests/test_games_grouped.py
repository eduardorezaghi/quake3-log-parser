from src.dclasses import QuakeLog
from src.parser import QuakeLogParser


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
