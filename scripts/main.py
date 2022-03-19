"""
nfl events parser

This command line application allows the user to enter a start
date and delta (in days after the start date) to retrieve the 
stats about games held between those days. Results also include
stats about the teams who played in these games.

Example of what the user might enter at the command line:
> python main.py 2020-01-12 7

The output of the application is a formatted json file which can
be found in nfl/output_data/. 

A key requirement of the application is the requests module. 
Requests are made to two seperate endpoints. Results are then 
transformed and combined before the final json file is output.
"""

import sys
from typing import List

from nfl.core import pull_json_data, transform_json_data, load_out_json_data
from nfl.helpers.command_line import check_command_line_arguments


def main(argc: int, argv: List[str]):
    """Runs a pipeline to pull, transform, and dump nfl data."""

    check_command_line_arguments(argc, argv)
    start_date, delta = argv[1], argv[2]

    # pull data >>> transform pulled data >>> dump transformed data
    scoreboard_data, team_ranking_data = pull_json_data(start_date, delta)
    transformed_data = transform_json_data(scoreboard_data, team_ranking_data)
    load_out_json_data(transformed_data)


if __name__ == "__main__":
    argv, argc = sys.argv, len(sys.argv)

    main(argc, argv)

    sys.exit(0)
