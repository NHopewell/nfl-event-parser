"""
core.py

Provides three main functionalities which, together, act as a
data extract, transformation, and load pipeline for the nfl api.
    1) pull data from scoreboard and rankings endpoints.
    2) transform and combine response data into the format displayed 
        in the json files found in nfl/output_data.
    3) load the transformed reponse data to nfl/output_data.

As with any pipeline, it is intended that these core three functions
(pull_json_data(), transform_json_data(), load_out_json_data())
take as input the returned value of the previous. This high level
3-step pipeline should be the crux of main().
"""

import requests, os, json, datetime
from typing import Dict, Optional, Tuple, List, Union

from nfl.helpers.dictionaries import load_config_constants, filter_dictionary
from nfl.helpers.dates import generate_end_date, split_datetime, add_date_and_time
from nfl.logger import Logger

# _extract_scoreboard_fields_of_interest() and _extract_rankings_fields_of_interest()
# rely some of the global scope constants below within their function bodies. Other
# functions in core.py use these constants as default values of their formal params.
API_KEY, SCOREBOARD, RANKINGS, OUTPUT_DIRECTORY = load_config_constants()


# our core data structure is a dict with string keys and string | list(string) values
json_data = Dict[str, Union[str, List[str]]]


def _extract_scoreboard_fields_of_interest(
    complete_scoreboard_data: json_data,
) -> List[json_data]:
    """Keeps only scoreboard fields of interest specified in config.json.

    If an entry in the scoreboard data pulled contains an empty collection
    (indicating a day where no game was played), this entry is not included
    in the returned list of entries.

    :param complete_scoreboard_data: unfiltered scoreboard data.
    :returns: a list of dictionaries representing filtered scoreboard data.
    """

    scoreboard_fields_of_interest = SCOREBOARD["fields_of_interest"]
    filtered_scoreboard_data = []

    # filter results keeping only fields specified in config.json
    for entry in complete_scoreboard_data:
        if (event_results := complete_scoreboard_data[entry]) :
            for event_id, event_data in event_results["data"].items():
                filtered_event_data = filter_dictionary(
                    event_data, scoreboard_fields_of_interest
                )
                filtered_event_data.update({"event_id": event_id})
                filtered_scoreboard_data.append(filtered_event_data)

    return filtered_scoreboard_data


def _extract_rankings_fields_of_interest(
    complete_rankings_data: json_data,
) -> List[json_data]:
    """Keeps only team ranking fields of interest specified in config.json.

    :param complete_rankings_data: unfiltered team rankings data.
    :returns: a list of dictionaries representing filtered ranking data.
    """

    rankings_fields_of_interest = RANKINGS["fields_of_interest"]
    filtered_ranking_data = []

    # filter results keeping only fields specified in config.json
    for team_data in complete_rankings_data["data"]:
        filtered_team_data = filter_dictionary(team_data, rankings_fields_of_interest)
        filtered_ranking_data.append(filtered_team_data)

    return filtered_ranking_data


def _pull_scoreboard_data(
    start_date: str,
    delta: str,
    endpoint: Optional[str] = SCOREBOARD["endpoint"],
    api_key: Optional[str] = API_KEY,
) -> List[json_data]:
    """Retrieves and filters data from scoreboard endpoint of nfl api.

    The scoreboard endpoint must be imputed with start and end dates
    representing the number of days worth of data to pull.

    :param start_date: the first day of scoreboard data to pull.
    :param delta: The number of days worth of data to pull. Delta
        must be between 0 and 7 days inclusive.
    :param endpoint: The incomplete scoreboard enpoint, not including
        the start and end dates.
    :param api_key: An api key to access the nfl api.
    :returns: a list of dictionaries representing all scoreboard data.
    """

    endpoint, extension = os.path.splitext(endpoint)
    end_date = generate_end_date(start_date, delta)
    endpoint_with_dates_imputed = (
        f"{'/'.join([endpoint, start_date, end_date])}{extension}"
    )

    try:
        response = requests.get(
            endpoint_with_dates_imputed, params={"api_key": API_KEY}
        )

        if response.ok:
            response = response.json()
            scoreboard_results = response["results"]
            filtered_scoreboard_data = _extract_scoreboard_fields_of_interest(
                scoreboard_results
            )

            return filtered_scoreboard_data
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def _pull_team_rankings(
    endpoint: Optional[str] = RANKINGS["endpoint"], api_key: Optional[str] = API_KEY
) -> List[json_data]:
    """Retrieves and filters data from rankings endpoint of nfl api.

    :param endpoint: The incomplete scoreboard enpoint, not including
        the start and end dates.
    :param api_key: An api key to access the nfl api.
    :returns: a list of dictionaries representing all rankings data.
    """
    try:
        response = requests.get(endpoint, params={"api_key": API_KEY})

        if response.ok:
            response = response.json()
            ranking_results = response["results"]
            filtered_ranking_data = _extract_rankings_fields_of_interest(
                ranking_results
            )

            return filtered_ranking_data
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


@Logger
def pull_json_data(
    start_date: str, delta: str
) -> Tuple[List[json_data], List[json_data]]:
    """Retrieves all data from scoreboard and rankings endpoints.

    :param start_date: the first day of scoreboard data to pull.
    :param delta: The number of days worth of data to pull. Delta
        must be between 0 and 7 days inclusive.
    :raises:
        ValueError:
            * If start date is in the wrong format.
            * If user input a delta outside of range 0-7.
            * If no scoreboard data was returned, likely
                indicating a provided date out of bounds.
    :returns: a tuple of lists containing scoreboard and rankings data.
    """

    scoreboard_data = None

    try:
        scoreboard_data = _pull_scoreboard_data(start_date, delta)
        team_ranking_data = _pull_team_rankings()
    except ValueError as ve:
        msg = "Please pass a correct starting date, such as 2000-12-20."
        msg = f"{ve}. {msg}"
        raise ValueError(msg)
    except TypeError:
        msg = "Must pass a time delta between 0 and 7 days (inclusive)."
        raise ValueError(msg)
    finally:
        if not scoreboard_data:
            msg = (
                "No scoreboard data was returned for the specified "
                "starting date and delta provided. Either no data exists, "
                "or a date out of range was entered by mistake. Please check "
                "that the starting date provided is correct."
            )
            raise ValueError(msg)

    return scoreboard_data, team_ranking_data


@Logger
def transform_json_data(
    scoreboard_data: List[json_data], team_rankings: List[json_data]
) -> List[json_data]:
    """Combines scoreboard and teamrankings data and reorders fields.

    The raw date pulled from the scoreboard endpoint contains a time
    component along with the date component. These two components are
    split into their own fields (date & time).

    A number of keys are assumed to exist in the input data, matching
    the nfl api response.

    :param scoreboard_data: scoreboard data post filtering.
    :param team_rankings: team rankings data post filtering.
    :returns: a list of dictionaries which are the combined scoreboard
        and rankings data.
    """

    transformed_result_list = []
    desired_key_order = [
        "event_id",
        "event_date",
        "event_time",
        "away_team_id",
        "away_nick_name",
        "away_city",
        "away_rank",
        "away_rank_points",
        "home_team_id",
        "home_nick_name",
        "home_city",
        "home_rank",
        "home_rank_points",
    ]
    # split default datetime field into two seperate fields (date & time)
    scoreboard_data = add_date_and_time(scoreboard_data)

    # match appropriate rankings data with each event
    for event in scoreboard_data:
        away_team_id, home_team_id = event["away_team_id"], event["home_team_id"]
        for team in team_rankings:
            if away_team_id == team["team_id"]:
                away_team_rank, away_team_points = team["rank"], team["adjusted_points"]
            elif home_team_id == team["team_id"]:
                home_team_rank, home_team_points = team["rank"], team["adjusted_points"]

        # update scoreboard data with rankings data
        event["away_rank"], event["away_rank_points"] = away_team_rank, away_team_points
        event["home_rank"], event["home_rank_points"] = home_team_rank, home_team_points

        # reorder keys to match the desired key ordering of our output
        ordered_output = {key: event[key] for key in desired_key_order}
        transformed_result_list.append(ordered_output)

    return transformed_result_list


@Logger
def load_out_json_data(
    combined_data: json_data, output_dir: Optional[str] = OUTPUT_DIRECTORY
) -> None:
    """Dumps final formatted data to a json file.

    :param combined_data: combined scoreboard and rankings data
        after tranformations applied.
    :param output_dir: a directory to dump to.
    """

    filename = str(datetime.datetime.now())

    with open(f"{output_dir}{filename}.json", "w") as outfile:
        json.dump(
            combined_data,
            outfile,
            indent=4,
        )
