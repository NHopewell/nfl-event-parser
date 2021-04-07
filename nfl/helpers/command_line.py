"""
command_line.py

Checks for improper command line arguments passed by user.
"""

from typing import List


def check_command_line_arguments(argc: int, argv: List[str]) -> None:
    """Checks the user input the proper command line args.

    :param argc: the number of command line arguments passed.
    :param argv: a list of positional command line arguments passed.
    :raises:
        ValueError:
            * The user does not provide a start date and delta.
            * The user provides a start date and delta, along with
                additional command line arguments.
            * The start date is not in the correct format (YYYY-MM-DD).
            * The user passes a delta outside of the range 0 through 7.
    """

    if not argc == 3:
        msg = (
            "The expected input includes starting date and a delta in days. "
            "Example: python main.py 2020-01-12 7"
        )
        raise ValueError(msg)

    if not len(argv[1].split("-")) == 3:
        msg = (
            "Please pass a starting date (including a year, month, "
            "and date) in the following format: YYYY-MM-DD."
        )
        raise ValueError(msg)

    if not int(argv[2]) in range(0, 8):
        msg = "The delta provided must be between 0 and 7 days inclusive."
        raise ValueError(msg)

    nfl_ascii = (
        "    _   __________               ______________  ___________ \n"
        "   / | / / ____/ /      __/|_   / ___/_  __/   |/_  __/ ___/ \n"
        "  /  |/ / /_  / /      |    /   \__ \ / / / /| | / /  \__ \ \n"
        " / /|  / __/ / /___   /_ __|   ___/ // / / ___ |/ /  ___/ / \n"
        "/_/ |_/_/   /_____/    |/     /____//_/ /_/  |_/_/  /____/ "
    )

    print(nfl_ascii)
