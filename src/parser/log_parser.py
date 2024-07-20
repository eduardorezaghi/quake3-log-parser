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
        self.log_file_path: Path = log_file_path
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
        # An end-game is a line with ShutdownGame or with hh:mm ------------------------------------------------------------ (60 dashes)
        # First, check if there is a game in progress, THEN check if the line is ShutdownGame OR a line with hh:mm ---- ...
        elif self.current_game and (
            re.search(r"ShutdownGame", line) or re.search(r"\d{2}:\d{2} -{60}", line)
        ):
            self._end_current_game()

    def _count_players(self, line) -> None:
        if re.search(r"ClientUserinfoChanged", line):
            # Extract the player name from the log line
            player = re.search(r"n\\([^\\]*)", line).group(1)
            self.current_game.players.add(player)

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

        return self._group_game_results()
