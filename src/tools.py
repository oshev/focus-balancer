from datetime import datetime, date, time, timedelta


def get_week_start() -> datetime:
    today_beginning = get_day_start()
    return today_beginning - timedelta(days=today_beginning.weekday())


def get_day_start() -> datetime:
    return datetime.combine(date.today(), time())


def secs_to_str(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return "{hours:02d}:{minutes:02d}:{secs:02d}"\
        .format(hours=hours, minutes=minutes, secs=seconds % 60)
