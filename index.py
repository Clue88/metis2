#! /usr/bin/python
print ('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from templates import render_template
from date import get_today_short, get_today_long, get_day_str

def main():
    replacements = {
        'username': 'Christopher',
        'date': get_today_long(),
        'day': get_day_str(get_today_short())
    }

    print(render_template('index.html', replacements))

main()
