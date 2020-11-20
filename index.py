# Copyright (c) 2020 Christopher Liu

#! /usr/bin/python3
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

import os
from templates import render_template, redirect
from date import get_today_short, get_today_long, get_day_str, get_day_info
from auth import check_login, get_id
from user import get_name, get_hw, get_tests
from schedules import get_schedules

def main():
    if not check_login():
        print(redirect('login.py'))
        return

    id = get_id()

    day_info = get_day_info(get_today_short())
    if day_info is not None:
        schedule = get_schedules(id, day_info[0], day_info[1], day_info[2])
    else:
        schedule = ''

    replacements = {
        'username': get_name(id),
        'date': get_today_long(),
        'day': get_day_str(get_today_short()),
        'schedule': schedule,
        'hw': get_hw(id),
        'tests': get_tests(id)
    }

    print(render_template('index.html', replacements))

main()
