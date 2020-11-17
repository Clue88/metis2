from datetime import date, datetime, timezone, timedelta
from config import *
import os
import calendar

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

def get_day_info(date):
    f = open(os.path.join('data', SCHEDULE_PATH))
    s = f.read()
    f.close()

    for line in s.split('\n')[0:-1]:
        if line.split(',')[0] == date:
            dl = line.split(',')
            return [dl[1], int(dl[2]), int(dl[3])]

    return None

def format_date(date):
    weekday = datetime.strptime(date, '%Y-%m-%d').weekday()
    weekday = calendar.day_name[weekday][0:3]
    year = date.split('-')[0][-2:]
    month = date.split('-')[1]
    if int(month) < 10:
        month = month[1:]
    day = date.split('-')[2]
    if int(day) < 10:
        day = day[1:]

    return weekday + ' ' + month + '/' + day + '/' + year

def unformat_date(date):
    date = date[4:]
    month = date.split('/')[0]
    day = date.split('/')[1]
    year = date.split('/')[2]

    if int(month) < 10:
        month = '0' + month
    if int(day) < 10:
        day = '0' + day
    year = '20' + year

    return year + '-' + month + '-' + day
