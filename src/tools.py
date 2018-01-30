from datetime import datetime, date, time, timedelta


def get_week_start() -> datetime:
    today_beginning = get_day_start()
    return today_beginning - timedelta(days=today_beginning.weekday())


def get_day_start() -> datetime:
    return datetime.combine(date.today(), time())
