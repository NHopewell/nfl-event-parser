"""
dictionaries.py

Contains helper functions for loading the json config file
and filtering dictionary keys.
"""

import json
from typing import Optional, Tuple, List


def load_config_constants(
    *keys, config_dir: Optional[str] = "config.json"
) -> Tuple[str]:
    """Loads and returns values of a config json file.

    :param *keys: a variable number of keys to retrieve values for.
    :param config_dir: the location of the config file.
    :returns: a tuple of strings representing the config values.
    """

    with open(config_dir) as json_file:
        config_json = json.load(json_file)

    if not keys:
        keys = ["API_KEY", "SCOREBOARD", "RANKINGS", "OUTPUT_DIRECTORY"]
    else:
        if not all(key in config_json for key in keys):
            msg = "One or more keys provided does not exist in config.json."
            raise ValueError(msg)

    constants = [config_json[key] for key in keys]

    return tuple(constants)


def filter_dictionary(dictionary: dict, keys_to_keep: List[str]) -> dict:
    """Removes unwanted key,value pairs from dict.

    :param dictionary: a dictionary to filter.
    :param keys_to_keep: keys of the dictionary to retain.
    :returns: a filtered dictionary
    """

    return {key: value for key, value in dictionary.items() if key in keys_to_keep}
