#! /usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

import os
from templates import render_template, redirect
from date import get_today_short, get_today_long, get_day_str
from auth import check_login

def main():
    if not check_login():
        print(redirect('login.py'))
        return

    replacements = {
        'username': 'Christopher',
        'date': get_today_long(),
        'day': get_day_str(get_today_short())
    }

    print(render_template('index.html', replacements))

main()
