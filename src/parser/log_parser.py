import re
from pathlib import Path
from typing import Generator

from src.dclasses import QuakeLog
from src.enums import QuakeDeathCause

from .base_parser import AbstractLogParser


class QuakeLogParser(AbstractLogParser):
    DEATH_CAUSE_MAP: dict[str, QuakeDeathCause] = {
        cause.value: cause for cause in QuakeDeathCause
    }

    def __init__(self, log_file_path: Path):
        super().__init__(log_file_path)
        self.log_file = open(log_file_path, "r")
        self.games: list[QuakeLog] = []
        self.current_game: QuakeLog | None = None

    def _line_parser(self) -> Generator[str, None, None]:
        with open(self.log_file_path, "r") as log_file:
            for line in log_file:
                yield line.strip()

    def _group_game_results(self) -> list[dict]:
        parsed_games = []
        for game in self.games:
            game_result = game.to_dict()
            parsed_games.append(game_result)

        return parsed_games

    def _count_games(self, line) -> None:
        if re.search(r"InitGame", line):
            self._start_new_game()
        # Catched a bug in the log! ShutdownGame is not always the end of a game.
        # An end-game is a line with ShutdownGame or with
        # First, check if there is a game in progress, THEN check if the line is ShutdownGame OR a line with hh:mm ---- ...
        elif self.current_game and (
            re.search(r"ShutdownGame", line) or re.search(r"\d+\s+\d+:\d+\s+-+", line)
        ):
            self._end_current_game()

    def _count_players(self, line) -> None:
        if re.search(r"ClientUserinfoChanged", line):
            # Extract the player name from the log line
            player = re.search(r"n\\([^\\]*)", line).group(1)
            self.current_game.players.add(player)

    def _count_kills(self, line) -> None:
        if re.search(r"Kill", line):
            # Extract the killer and victim names from the log line
            killer, victim = re.search(
                r"Kill: \d+ \d+ \d+: (.*) killed (.*) by", line
            ).groups()

            # Extract the death cause from the log line
            death_cause = re.search(r"by (.*)", line).group(1)
            death_cause = self.DEATH_CAUSE_MAP.get(
                death_cause, QuakeDeathCause.MOD_UNKNOWN
            )

            self.current_game.kills_score[killer] = (
                self.current_game.kills_score.get(killer, 0) + 1
            )
            self.current_game.kills_score[victim] = (
                self.current_game.kills_score.get(victim, 0) - 1
            )

            if killer != victim and killer != "<world>":
                self.current_game._total_kills += 1

    def _start_new_game(self) -> None:
        self.current_game = QuakeLog(game_id=len(self.games) + 1)

    def _end_current_game(self) -> None:
        if self.current_game:
            self.games.append(self.current_game)
            self.current_game = None

    def parse(self) -> list[dict]:
        for line in self._line_parser():
            self._count_games(line)
            self._count_players(line)
            self._count_kills(line)

        return self._group_game_results()
