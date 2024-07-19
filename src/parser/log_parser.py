import re
from src.dclasses import QuakeLog

from src.enums import QuakeDeathCause

from .base_parser import AbstractLogParser


class QuakeLogParser(AbstractLogParser):
    DEATH_CAUSE_MAP: dict[str, QuakeDeathCause] = {
        cause.value: cause for cause in QuakeDeathCause
    }

    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.log_file = open(log_file_path, "r")
        self.games: list[QuakeLog] = []
        self.current_game: QuakeLog | None = None

    def _line_parser(self):
        with open(self.log_file_path, "r") as log_file:
            for line in log_file:
                yield line.strip()

    def parse(self):
        for line in self._line_parser():
            self._count_games(line)

        return self._group_game_results()

    def _group_game_results(self):
        parsed_games = []
        for game in self.games:
            game_result = game.__dict__()
            parsed_games.append(game_result)

        return parsed_games

    def match_death_cause(self, log_line):
        pass

    def _count_games(self, line):
        if re.search(r"InitGame", line):
            self._start_new_game()
        elif re.search(r"ShutdownGame", line) and self.current_game:
            self._end_current_game()

    def _start_new_game(self):
        self.current_game = QuakeLog(game_id=len(self.games) + 1)

    def _end_current_game(self):
        if self.current_game:
            self.games.append(self.current_game)
            self.current_game = None
