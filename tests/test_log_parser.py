import pytest

from src.enums import QuakeDeathCause
from src.parser import QuakeLogParser


@pytest.fixture
def grouped_deaths_by_means_fixture(create_mock_log_file):
    content = ""
    for death_cause in QuakeDeathCause:
        content += (
            f"20:54 Kill: 1022 2 22: Killer killed Victim by {death_cause.value}\n"
        )

    yield content


def test_parse_grouped_deaths_by_means(
    create_mock_log_file, grouped_deaths_by_means_fixture
):
    # Arrange
    mock_file = create_mock_log_file(grouped_deaths_by_means_fixture)
    log_parser = QuakeLogParser(mock_file)
    log_parser._start_new_game()
    log_parser.games.append(log_parser.current_game)

    # Act
    grouped_deaths = log_parser.parse_grouped_deaths_by_means()
    log_parser._end_current_game()

    # Assert
    assert log_parser.games[0].get_total_kills == 28
    assert all(isinstance(game.get("game_1"), dict) for game in grouped_deaths)
    # Assert that each cause of death have '1' kill
    assert all(
        death.get("game_1").get("kills_by_means").get(cause.value) == 1
        for death in grouped_deaths
        for cause in QuakeDeathCause
    )


@pytest.fixture
def grouped_deaths_by_means_descending_order_fixture(create_mock_log_file):
    lines = [
        f"20:54 Kill: 1022 2 22: PlayerA killed PlayerB by {QuakeDeathCause.MOD_BFG.value}\n",
        f"20:54 Kill: 1022 2 22: PlayerB killed PlayerA by {QuakeDeathCause.MOD_BFG.value}\n",
        f"20:54 Kill: 1022 2 22: PlayerA killed PlayerB by {QuakeDeathCause.MOD_BFG.value}\n",
        f"20:54 Kill: 1022 2 22: PlayerA killed PlayerA by {QuakeDeathCause.MOD_BFG_SPLASH.value}\n",
        f"20:54 Kill: 1022 2 22: PlayerA killed PlayerB by {QuakeDeathCause.MOD_ROCKET.value}\n",
        f"20:54 Kill: 1022 2 22: PlayerA killed PlayerB by {QuakeDeathCause.MOD_ROCKET.value}\n",
        f"20:54 Kill: 1022 2 22: PlayerC killed PlayerD by {QuakeDeathCause.MOD_SHOTGUN.value}\n",
        f"20:54 Kill: 1022 2 22: PlayerA killed PlayerB by {QuakeDeathCause.MOD_PLASMA.value}\n",
    ]
    content = ""
    for line in lines:
        content += line

    yield content


def test_parse_grouped_deaths_by_means_descending_order(
    create_mock_log_file, grouped_deaths_by_means_descending_order_fixture
):
    # Arrange
    mock_file = create_mock_log_file(grouped_deaths_by_means_descending_order_fixture)
    log_parser = QuakeLogParser(mock_file)
    log_parser._start_new_game()
    log_parser.games.append(log_parser.current_game)

    # Act
    grouped_deaths = log_parser.parse_grouped_deaths_by_means()
    log_parser._end_current_game()

    # Assert
    assert log_parser.games[0].get_total_kills == 7
    assert all(isinstance(game.get("game_1"), dict) for game in grouped_deaths)
    # Assert that the self kill are not counted
    assert log_parser.games[0].get_kill_by_player.get("PlayerA") == 4

    # Assert that the kills are in descending order
    assert list(grouped_deaths[0].get("game_1").get("kills_by_means").values()) == [
        3,
        2,
        1,
        1,
    ]
