# focus-balancer
A command-line tool, which helps your define your focus areas and easily monitor them based on your Toggl data.

Define the structure of your dashboard in `configs/dashboard.yaml` (See example in `dashboard.yaml`)

Details:
- `Stats` allows you to choose which statistics to show for your leaf categories on the dashboard and in which order.
    - DayTime - time you spent on the leaf category today.
    - DayGoal - minimum time you want to spend on this category per day.
    - WeekTime - time you spent on the leaf category this week.
    - WeekGoal - minimum time you want to spend on this category per week.
    - WeekDays - how many days you did anything for this category this week.
    - LastTime - last time (this week) you touched this category.
- `Leaf` indicates a new leaf category in the dashboard tree.
    - `Link` indicates to add a URL anchor to the leaf.
    - `DayGoal` defines minimum time you want to spend on this category per day.
    - `WeekGoal` defines minimum time you want to spend on this category per week.
    - `Tags` comma-separated tags which define this category - a Toggle time entry which has all these tags will be attributed to this category (AND).
        - In case several `Tags` properties per leaf define, a Toggle time entry which has all tags from any of the Tag lines defined for the leaf will be attributed to this category (OR).     
    - `TitleRegex`: regular expression which defines this category - a Toggle time entry which matches this expression will be attributed to this category.
        - Several `TitleRegex` lines will be treated as OR (same as for `Tags`).
    - In case both `Tags` and `TitleRegex` are defined, then both conditions must be true to attribute an entry to this category.  


**Warning**: The tool is still in active development. See TODO list in `src/focus_balancer.py`.

Get your Toggle API Token from your [Toggle profile page](https://toggl.com/app/profile) (in the bottom)

Run the tool: `python3 focus_balancer.py --token YOUR_TOGGL_API_TOKEN`


Focus Balancer will generate an HTML dashboard and save it in `focus_balancer.html`
    