# NFL events parser

This repo is a simple example of a backend service which pulls from a remote API that is frequently updated, transforms the reponse JSON data, and dumps the transformed results to a file. I am not an NFL fan, this is merely a small example which showcases that I can write, document, and test clean Pythonic code. 

## The Service

A fake client wants us to develop a process which returns a list of NFL event and team ranking data in JSON format between a time period of 1 to 7 days. In order to do so, we need to pull from two API endpoints provided by https://delivery.chalk247.com/ and combine 
results.

The response data from the API does not match the output format our client wants. We must transform and restructure the response data to suit our clients desired format, seen below.

Here is an example reponse for the week ```2020-01-12``` to ```2020-01-19``` (four games were played in total, two on the 12th, two on the 19th):

```json
[
    {
        "event_id": "1233827",
        "event_date": "12-01-2020",
        "event_time": "15:05",
        "away_team_id": "42",
        "away_nick_name": "Texans",
        "away_city": "Houston",
        "away_rank": "25",
        "away_rank_points": "-6.410",
        "home_team_id": "63",
        "home_nick_name": "Chiefs",
        "home_city": "Kansas City",
        "home_rank": "5",
        "home_rank_points": "11.375"
    },
    {
        "event_id": "1233912",
        "event_date": "12-01-2020",
        "event_time": "18:40",
        "away_team_id": "52",
        "away_nick_name": "Seahawks",
        "away_city": "Seattle",
        "away_rank": "10",
        "away_rank_points": "7.970",
        "home_team_id": "39",
        "home_nick_name": "Packers",
        "home_city": "Green Bay",
        "home_rank": "4",
        "home_rank_points": "13.112"
    },
    {
        "event_id": "1234560",
        "event_date": "19-01-2020",
        "event_time": "15:05",
        "away_team_id": "62",
        "away_nick_name": "Titans",
        "away_city": "Tennessee",
        "away_rank": "18",
        "away_rank_points": "-0.970",
        "home_team_id": "63",
        "home_nick_name": "Chiefs",
        "home_city": "Kansas City",
        "home_rank": "5",
        "home_rank_points": "11.375"
    },
    {
        "event_id": "1234565",
        "event_date": "19-01-2020",
        "event_time": "18:40",
        "away_team_id": "39",
        "away_nick_name": "Packers",
        "away_city": "Green Bay",
        "away_rank": "4",
        "away_rank_points": "13.112",
        "home_team_id": "58",
        "home_nick_name": "49ers",
        "home_city": "San Francisco",
        "home_rank": "20",
        "home_rank_points": "-2.697"
    }
]
```

## How to Run

This is a command line application, it is expected that the user input a start date and a delta (in days, between 0 and 7 inclusive).

Clone the repository, activate a virtual env, and install the requirements.
* on macOS and Linux:
```shell
python -m venv env

source env/bin/activate

pip install -r requirements.txt
```

* on Windows:
```shell
py -m venv env

.\env\Scripts\activate

pip install -r requirements.txt
```

Run with a start date and delta:
```shell
python main.py 2020-01-12 7
```

If you passed valid arguments at the command line, you will see the following ascii art printed in the console:
```
    _   __________               ______________  ___________ 
   / | / / ____/ /      __/|_   / ___/_  __/   |/_  __/ ___/
  /  |/ / /_  / /      |    /   \__ \ / / / /| | / /  \__ \
 / /|  / __/ / /___   /_ __|   ___/ // / / ___ |/ /  ___/ /
/_/ |_/_/   /_____/    |/     /____//_/ /_/  |_/_/  /____/
```

### How to run tests

Tests can be found in ```tests/```. From the root directory, run ```pytest -v```, pytest will automatically find and run the tests.

### Note about the API key

**You don't have to get your own API key**, I did not gitignore the API key as per the standard protocol. It is exposed not only to the application at run time but also anyone viewing this repository. It is an open API and not neccessary to hide it for this example service.

## Output

The output data automatically gets dumped into ```output_data/todays_date_and_time.json```.

