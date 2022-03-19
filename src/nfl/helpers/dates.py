"""
dates.py

Provides functionality for working with dates such as generating
an end date based on a start date and a delta, splitting a datetime
field into seperate date and time fields, as well as adding date 
and time keys, value pairs to a dictionary containing a datetime field.
"""

from typing import Optional, Tuple, List, Dict, Union
from datetime import datetime, timedelta

json_data = Dict[str, Union[str, List[str]]]


def generate_end_date(
    start_date: str, delta: str, date_format: Optional[str] = "%Y-%m-%d"
) -> str:
    """Generates an end date based on a start date and delta.

    :param start_date: a starting date.
    :param delta: a delta representing a number of days from the start date.
    :param date_format: a date format the start date adheres to.
    :returns: A string representing the end date.
    """

    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strftime(start_date + timedelta(days=int(delta)), date_format)

    return end_date


def split_datetime(
    date_time: str, datetime_format: Optional[str] = "%Y-%m-%d %H:%M"
) -> Tuple[str, str]:
    """Split a datetime string into date and time components.

    :param date_time: a string containing a date and time.
    :datetime_format:  a datetime format that date_time adheres to.
    :returns: A tuple of strings reprsenting the date and time.
    """

    fulldate = datetime.strptime(date_time, datetime_format)
    date = fulldate.strftime("%d-%m-%Y")
    time = fulldate.strftime("%H:%M")

    return date, time


def add_date_and_time(response_data: List[json_data]) -> List[json_data]:
    """Adds date and time key,value pairs to a list of dictionaries.

    It is assumed that each dictionary contains an "event_date"
    key, matching the response from the scoreboard endpoint of
    the nfl api.

    :param reponse_data: A list of dictionaries representing event
        data pulled from the nfl scorebord endpoint.
    :raises:
        KeyError: if event_date key not found.
    :returns: list of event data with date and time added.
    """

    for response in response_data:
        try:
            event_date, event_time = split_datetime(response["event_date"])
            response["event_date"], response["event_time"] = event_date, event_time
        except KeyError:
            msg = (
                "event_date column not present in response fields provided. "
                "Check config.json to ensure it was not removed from "
                "SCOREBOARD['fields_of_interest']."
            )
            raise KeyError(msg)

    return response_data
