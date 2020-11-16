#! /usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from templates import render_template
from schedules import period_forms
from config import *
from auth import get_existing_emails

def main():
    replacements = {
        'emails': get_existing_emails(),
        'periods': period_forms(NUM_PERIODS)
    }
    print(render_template('register.html', replacements))

main()
