from datetime import date, datetime, timezone, timedelta
from config import *
import os

def get_today_short():
    today = datetime.now(tz=timezone(timedelta(hours=TZ_OFFSET), TZ_NAME))
    format_today = today.strftime('%-m/%-d/%y')
    return str(format_today)

def get_today_long():
    today = datetime.now(tz=timezone(timedelta(hours=TZ_OFFSET), TZ_NAME))
    format_today = today.strftime('%A, %B %-d, %Y')
    return str(format_today)

def get_day_str(date):
    f = open(os.path.join('data', SCHEDULE_PATH))
    s = f.read()
    f.close()

    for line in s.split('\n')[0:-1]:
        if line.split(',')[0] == date:
            dl = line.split(',')
            return dl[1] + ' Day (' + dl[2] + '-' + dl[3] + ')'

    return 'No school today!'
