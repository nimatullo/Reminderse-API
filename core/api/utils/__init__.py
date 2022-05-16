from datetime import datetime


def validate_date(date):
    if date:
        return datetime.strptime(date, "%Y-%m-%d")
    else:
        return None
