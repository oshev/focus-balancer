from contextlib import ContextDecorator
from datetime import datetime, date, time, timedelta
import calendar


def get_week_start() -> datetime:
    today_beginning = get_day_start()
    return today_beginning - timedelta(days=today_beginning.weekday())


def get_day_start() -> datetime:
    return datetime.combine(date.today(), time())


def secs_to_str(seconds: int) -> str:
    if seconds == 0:
        return "-"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return "{hours:02d}:{minutes:02d}".format(hours=hours, minutes=minutes)


class EmptyContext(ContextDecorator):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


weekdays_str = list(calendar.day_abbr)