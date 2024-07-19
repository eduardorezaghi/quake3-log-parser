import re

from src.enums import QuakeDeathCause

from .base_parser import AbstractLogParser


class QuakeLogParser(AbstractLogParser):
    DEATH_CAUSE_MAP: dict[str, QuakeDeathCause] = {
        cause.value: cause for cause in QuakeDeathCause
    }

    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.log_file = open(log_file_path, "r")
        self.game_count = 0
        self.games = []
        self.current_game = False

    def _line_parser(self):
        with open(self.log_file_path, "r") as log_file:
            for line in log_file:
                yield line.strip()

    def parse(self):
        for line in self._line_parser():
            self._count_games(line)

        return {"game_count": self.game_count}

    def match_death_cause(self, log_line):
        pass

    def _count_games(self, line):
        if re.search(r"InitGame", line):
            self.current_game = True
        elif re.search(r"ShutdownGame", line) and self.current_game:
            self.game_count += 1
            self.current_game = False

    def _get_world_kill_count(self): ...
