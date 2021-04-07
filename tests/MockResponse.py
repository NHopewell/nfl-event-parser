from typing import Dict, Union, List, Optional
import json

json_data = Dict[str, Union[str, List[str]]]

with open("tests/static_response.json") as json_file:
    response_body = json.load(json_file)


class MockScoreboardResponse:
    """Mock response json data from scoreboard endpoint."""
    def __init__(self, body: Optional[json_data] = response_body):
        self.status_code = 200
        self.ok = True
        self.body = body

    def json(self):
        return self.body

    def raise_for_status(self):
        return self.status_code
