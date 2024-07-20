import argparse
import json
from pathlib import Path

from src.dclasses import QuakeLogEncoder
from src.parser import QuakeLogParser


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse a Quake log file.")
    parser.add_argument("log_file", type=str, help="Path to the Quake log file")
    parser.add_argument(
        "--group-deaths", action="store_true", help="Group deaths by means"
    )
    return parser.parse_args()


def run(args):
    log_file_path = Path(args.log_file)

    if not log_file_path.is_file():
        raise FileNotFoundError(f"Error: The file {log_file_path} does not exist.")

    parser = QuakeLogParser(log_file_path)

    parser.parse()
    if args.group_deaths:
        output = parser._group_deaths_by_means()
    else:
        output = parser.games

    print(json.dumps(output, indent=4, cls=QuakeLogEncoder))


if __name__ == "__main__":
    run(parse_arguments())
