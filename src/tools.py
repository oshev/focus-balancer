from datetime import datetime, date, time, timedelta


def get_week_start() -> datetime:
    today_beginning = datetime.combine(date.today(), time())
    return today_beginning - timedelta(days=today_beginning.weekday())
