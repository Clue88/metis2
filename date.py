from datetime import date, datetime, timezone, timedelta
from config import *

def get_today():
    today = datetime.now(tz=timezone(timedelta(hours=TZ_OFFSET), TZ_NAME))
    format_today = today.strftime('%A, %B %-d, %Y')
    return str(format_today)
