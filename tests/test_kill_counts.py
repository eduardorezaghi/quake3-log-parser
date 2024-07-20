import pytest

from src.dclasses import QuakeLog
from src.enums import QuakeDeathCause
from src.parser import QuakeLogParser


@pytest.fixture
def log_parser(tmp_path):
    file_path = tmp_path / "test.log"
    file_content = "foo"
    file_path.write_text(file_content)
    yield QuakeLogParser(file_path)


def test_count_kills_with_kill_line(log_parser):
    line = f"20:54 Kill: 1022 2 22: <world> killed Isgalamido by {QuakeDeathCause.MOD_TRIGGER_HURT.value}"
    log_parser.current_game = QuakeLog(game_id=1)
    log_parser.current_game.kills = {"<world>": 0, "Isgalamido": 0}

    log_parser._count_kills(line)

    assert log_parser.current_game.kills == {"<world>": 1, "Isgalamido": -1}


def test_count_kills_with_self_kill(log_parser):
    line = f"20:54 Kill: 1022 2 22: Isgalamido killed Isgalamido by {QuakeDeathCause.MOD_SUICIDE.value}"
    log_parser.current_game = QuakeLog(game_id=1)
    log_parser.current_game.kills = {"Isgalamido": 0}

    log_parser._count_kills(line)

    assert log_parser.current_game.kills == {"Isgalamido": 0}
    assert log_parser.current_game.total_kills == 0


def test_count_kills_with_unknown_death_cause(log_parser):
    line = f"20:54 Kill: 1022 2 22: Isgalamido killed Victim by {QuakeDeathCause.MOD_UNKNOWN.value}"
    log_parser.current_game = QuakeLog(game_id=1)
    log_parser.current_game.kills = {"Isgalamido": 0, "Victim": 0}

    log_parser._count_kills(line)

    assert log_parser.current_game.kills == {"Isgalamido": 1, "Victim": -1}
    assert log_parser.current_game.total_kills == 1


def test_count_kills_with_existing_killer_and_victim(log_parser):
    line = f"20:54 Kill: 1022 2 22: Killer killed Victim by {QuakeDeathCause.MOD_CHAINGUN.value}"
    log_parser.current_game = QuakeLog(game_id=1)
    log_parser.current_game.kills = {"Killer": 10, "Victim": -3}

    log_parser._count_kills(line)

    assert log_parser.current_game.kills == {"Killer": 11, "Victim": -4}
    assert log_parser.current_game.total_kills == 1


def test_parse_kills_from_log_file(kill_counts_fixture):
    file_path, expected_kill_counts = kill_counts_fixture
    parser = QuakeLogParser(file_path)

    parser.parse()

    assert parser.games[0].total_kills == expected_kill_counts
