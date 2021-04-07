from unittest.mock import Mock, patch

from nfl.core import _pull_scoreboard_data
from tests.MockResponse import MockScoreboardResponse
from tests.mock_config import mock_scoreboard_config


@patch("nfl.helpers.dictionaries.load_config_constants")
@patch("nfl.core.requests.get")
def test_pull_scoreboard_data_response_exists(mock_response, mock_config):

    scorboard_mock = MockScoreboardResponse()
    attrs = {"ok": scorboard_mock.ok, "json.return_value": scorboard_mock.json()}
    mock_response.return_value = Mock(**attrs)

    mock_config = Mock()
    mock_config.return_value = mock_scoreboard_config()

    res = _pull_scoreboard_data("2020-01-12", "7")

    assert res


@patch("nfl.helpers.dictionaries.load_config_constants")
@patch("nfl.core.requests.get")
def test_pull_scoreboard_data_retains_only_fields_of_interest(
    mock_response, mock_config
):

    scorboard_mock = MockScoreboardResponse()
    attrs = {"ok": scorboard_mock.ok, "json.return_value": scorboard_mock.json()}
    mock_response.return_value = Mock(**attrs)

    mock_config = Mock()
    mock_config.return_value = mock_scoreboard_config()

    res = _pull_scoreboard_data("2020-01-12", "7")

    fields_of_interest = [
        "event_id",
        "event_date",
        "away_team_id",
        "away_nick_name",
        "away_city",
        "home_team_id",
        "home_nick_name",
        "home_city",
    ]

    assert all(field in fields_of_interest for event in res for field in event)
