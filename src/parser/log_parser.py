from .base_parser import AbstractLogParser, QuakeDeathCause


class QuakeLogParser(AbstractLogParser):
    DEATH_CAUSE_MAP: dict[str, QuakeDeathCause] = {
        cause.value: cause for cause in QuakeDeathCause
    }

    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.log_file = open(log_file_path, 'r')

    def _line_parser(self, line):
        return super()._line_parser(line)

    def parse(self):
        return super().parse()

    def match_death_cause(self, log_line):
        pass
