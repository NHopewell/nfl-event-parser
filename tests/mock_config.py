def mock_scoreboard_config():
    api_key = "74db8efa2a6db279393b433d97c2bc843f8e32b0"
    score_board = {
        "SCOREBOARD": {
            "endpoint": "https://delivery.chalk247.com/scoreboard/NFL.json",
            "fields_of_interest": [
                "event_id",
                "event_date",
                "away_team_id",
                "away_nick_name",
                "away_city",
                "home_team_id",
                "home_nick_name",
                "home_city",
            ],
        }
    }

    return api_key, score_board, None, None
