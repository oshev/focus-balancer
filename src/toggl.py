import json
from datetime import datetime

import requests

TOGGL_URL_TEMPLATE = "https://www.toggl.com/api/v8/time_entries?start_date={}&end_date={}"
TOGGL_TIME_FORMAT = "%Y-%m-%dT%H:%M:00Z"
TOGGL_ENTRY_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S+00:00"  # 2018-01-29T08:10:49+00:00


class TogglEntry:
    def __init__(self, entry_dict):
        if "description" in entry_dict:
            self.title = entry_dict["description"]
        else:
            self.title = None
        if "tags" in entry_dict:
            self.tags = entry_dict["tags"]
        else:
            self.tags = None
        self.start_datetime = datetime.strptime(entry_dict["start"], TOGGL_ENTRY_TIME_FORMAT)
        if "stop" in entry_dict:
            self.stop_datetime = datetime.strptime(entry_dict["stop"], TOGGL_ENTRY_TIME_FORMAT)
        else:
            self.stop_datetime = datetime.now()
        self.duration = entry_dict["duration"]


class Toggl:
    def __init__(self, api_token):
        self.api_token = api_token

    def get_entries(self, start_date: datetime,
                    end_date: datetime = datetime.now()):

        start_date_str = start_date.strftime(TOGGL_TIME_FORMAT)
        end_date_str = end_date.strftime(TOGGL_TIME_FORMAT)

        response = requests.get(TOGGL_URL_TEMPLATE.format(start_date_str, end_date_str),
                                auth=(self.api_token, 'api_token'))

        if response.status_code == 200:
            time_entries = json.loads(response.text)
            print("Got {} time entries".format(len(time_entries)))
            return time_entries
        else:
            print("Get error code from the API: {}".format(response.status_code))
            return []
