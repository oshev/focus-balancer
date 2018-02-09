import argparse
from _datetime import datetime

from src.dashboard_config import DashboardConfig
from src.toggl import Toggl
from src.tools import get_week_start
import os


project_dir = os.path.join(os.path.dirname(__file__), os.pardir)

OUTPUT_FILENAME = os.path.join(project_dir, "focus.html")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='Your API token; take it from https://toggl.com/app/profile',
                        required=True, default=None)
    parser.add_argument('-o', '--output_filename', help='Output file name',
                        required=False, default=OUTPUT_FILENAME)
    args = parser.parse_args()

    toggl = Toggl(args.token)
    entries = toggl.get_entries(start_date=get_week_start(), end_date=datetime.now())

    dashboard = DashboardConfig()

    for entry in entries:
        dashboard.register_entry(entry)

    html = dashboard.generate_html()
    with open(args.output_filename, "w") as output_file:
        output_file.write(html)

    print("Finished generating the HTML focus report.")

