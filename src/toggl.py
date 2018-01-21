import json
from datetime import datetime

import requests

TOGGL_URL_TEMPLATE = "https://www.toggl.com/api/v8/time_entries?start_date={}&end_date={}"
TOGGL_TIME_FORMAT = "%Y-%m-%dT%H:%M:00Z"


class Toggl:
    def __init__(self, api_token):
        self.api_token = api_token

    def get_entries(self, start_date: datetime,
                    end_date: datetime = datetime.now()):

        start_date_str = start_date.strftime(TOGGL_TIME_FORMAT.format(TOGGL_TIME_FORMAT))
        end_date_str = end_date.strftime(TOGGL_TIME_FORMAT.format(TOGGL_TIME_FORMAT))

        response = requests.get(TOGGL_URL_TEMPLATE.format(start_date_str, end_date_str),
                                auth=(self.api_token, 'api_token'))

        if response.status_code == 200:
            time_entries = json.loads(response.text)
            print("Got {} time entries".format(len(time_entries)))
            return time_entries
        else:
            print("Get error code from the API: {}".format(response.status_code))
            return []
