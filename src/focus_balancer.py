import argparse
from _datetime import datetime

from src.dashboard_config import DashboardConfig
from src.toggl import Toggl
from src.tools import get_week_start

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='Your API token; take it from https://toggl.com/app/profile',
                        required=True, default=None)
    args = parser.parse_args()

    toggl = Toggl(args.token)
    entries = toggl.get_entries(start_date=get_week_start(), end_date=datetime.now())

    dashboard = DashboardConfig()

    for entry in entries:
        dashboard.register_entry(entry)

    # TODO: Sorting Toggl entries into Category buckets based on the config

    # TODO: Scratch off completed categories

    # TODO: Generating HTML dashboard
