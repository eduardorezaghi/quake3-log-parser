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
    log_parser.current_game.kills_score = {"<world>": 0, "Isgalamido": 0}

    log_parser._count_kills(line)

    assert log_parser.current_game.kills_score == {"<world>": 1, "Isgalamido": -1}
    assert log_parser.current_game.get_total_kills == 1


def test_count_kills_with_self_kill(log_parser):
    line = f"20:54 Kill: 1022 2 22: Isgalamido killed Isgalamido by {QuakeDeathCause.MOD_SUICIDE.value}"
    log_parser.current_game = QuakeLog(game_id=1)
    log_parser.current_game.kills_score = {"Isgalamido": 0}

    log_parser._count_kills(line)

    assert log_parser.current_game.kills_score == {"Isgalamido": 0}
    assert log_parser.current_game.get_total_kills == 0


def test_count_kills_with_unknown_death_cause(log_parser):
    line = f"20:54 Kill: 1022 2 22: Isgalamido killed Victim by {QuakeDeathCause.MOD_UNKNOWN.value}"
    log_parser.current_game = QuakeLog(game_id=1)
    log_parser.current_game.kills_score = {"Isgalamido": 0, "Victim": 0}

    log_parser._count_kills(line)

    assert log_parser.current_game.kills_score == {"Isgalamido": 1, "Victim": -1}
    assert log_parser.current_game.get_total_kills == 1


def test_count_kills_with_existing_killer_and_victim(log_parser):
    line = f"20:54 Kill: 1022 2 22: Killer killed Victim by {QuakeDeathCause.MOD_CHAINGUN.value}"
    log_parser.current_game = QuakeLog(game_id=1)
    log_parser.current_game.kills_score = {"Killer": 10, "Victim": -3}

    log_parser._count_kills(line)

    assert log_parser.current_game.kills_score == {"Killer": 11, "Victim": -4}
    assert log_parser.current_game.get_total_kills == 1


def test_kill_counts_with_world_kill(log_parser):
    lines = [
        f"20:54 Kill: 1022 2 22: <world> killed Isgalamido by {QuakeDeathCause.MOD_TRIGGER_HURT.value}",
        f"20:54 Kill: 1022 2 22: <world> killed Isgalamido by {QuakeDeathCause.MOD_TRIGGER_HURT.value}",
        f"20:54 Kill: 1022 2 22: <world> killed Isgalamido by {QuakeDeathCause.MOD_TRIGGER_HURT.value}",
        f"20:54 Kill: 1022 2 22: Isgalamido killed Isgalamido by {QuakeDeathCause.MOD_BFG_SPLASH.value}",
        f"20:54 Kill: 1022 2 22: Isgalamido killed Zeh by {QuakeDeathCause.MOD_SHOTGUN.value}",
    ]
    log_parser.current_game = QuakeLog(game_id=1)
    log_parser.current_game.kills_score = {"<world>": 0, "Isgalamido": 0, "Zeh": 0}

    for line in lines:
        log_parser._count_kills(line)

    assert log_parser.current_game.kills_score == {
        "<world>": 3,
        "Isgalamido": -2,
        "Zeh": -1,
    }
    assert log_parser.current_game.get_total_kills == 4


def test_kill_counts_with_self_kills(log_parser):
    lines = [
        f"20:54 Kill: 1022 2 22: Isgalamido killed Isgalamido by {QuakeDeathCause.MOD_BFG_SPLASH.value}",
        f"20:54 Kill: 1022 2 22: Zeh killed Zeh by {QuakeDeathCause.MOD_ROCKET_SPLASH.value}",
        f"20:54 Kill: 1022 2 22: Mocinha killed Mocinha by {QuakeDeathCause.MOD_GRENADE_SPLASH.value}",
        f"20:54 Kill: 1022 2 22: Assasin killed Assasin by {QuakeDeathCause.MOD_LIGHTNING.value}",
    ]
    log_parser.current_game = QuakeLog(
        game_id=1, players={"Isgalamido", "Zeh", "Mocinha", "Assasin"}
    )
    log_parser.current_game.kills_score = {"<world>": 0, "Isgalamido": 0, "Zeh": 0}

    for line in lines:
        log_parser._count_kills(line)

    assert log_parser.current_game.players == {
        "Isgalamido",
        "Zeh",
        "Mocinha",
        "Assasin",
    }
    assert log_parser.current_game.kills_score == {
        "<world>": 0,
        "Isgalamido": 0,
        "Zeh": 0,
        "Mocinha": 0,
        "Assasin": 0,
    }
    assert log_parser.current_game.get_total_kills == 0


def test_parse_kills_from_log_file(kill_counts_fixture):
    file_path, expected_kill_counts = kill_counts_fixture
    parser = QuakeLogParser(file_path)

    parser.parse()

    assert parser.games[0].get_total_kills == expected_kill_counts
