import argparse

from _datetime import datetime

from src.toggl import Toggl
from src.tools import get_week_start

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='Your API token; take it from https://toggl.com/app/profile',
                        required=True, default=None)
    args = parser.parse_args()

    toggl = Toggl(args.token)
    entries = toggl.get_entries(start_date=get_week_start(), end_date=datetime.now())

    # TODO: Reading the config from YAML

    # TODO: Sorting Toggl entries into Category buckets based on the config

    # TODO: Scratch off completed categories

    # TODO: Generating HTML dashboard
