import abc
from pathlib import Path


class AbstractLogParser(abc.ABC):
    """
    Abstract class for log parsers.
    Defines the behaviour for concrete classes that implements it.
    """

    def __init__(self, log_file_path):
        """
        Constructor for the AbstractLogParser class.
        :param log_file_path: The path to the log file to be parsed.
        """
        self.log_file_path = Path(log_file_path)

    @abc.abstractmethod
    def _line_parser(self, line):
        """
        Method to parse a line of the log file.
        """
        pass

    @abc.abstractmethod
    def parse(self):
        """
        Abstract method to parse the log file.
        :return: A list of dictionaries, where each dictionary represents a log entry.
        """
        pass
