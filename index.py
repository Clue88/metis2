#! /usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

import os
from templates import render_template, redirect
from date import get_today_short, get_today_long, get_day_str, get_day_info
from auth import check_login
from user import get_name
from schedules import get_schedules

def main():
    if not check_login():
        print(redirect('login.py'))
        return

    id = ''
    cookies = os.environ['HTTP_COOKIE'].split(';')
    for cookie in cookies:
            if cookie.split('=')[0] == 'token':
                id = cookie.split('=')[1]

    day_info = get_day_info(get_today_short())
    if day_info is not None:
        schedule = get_schedules(id, day_info[0], day_info[1], day_info[2])
    else:
        schedule = ''

    replacements = {
        'username': get_name(id),
        'date': get_today_long(),
        'day': get_day_str(get_today_short()),
        'schedule': schedule
    }

    print(render_template('index.html', replacements))

main()
