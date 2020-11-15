#! /usr/bin/python
print ('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from templates import render_template
from date import get_today

def main():
    replacements = {
        'username': 'Christopher',
        'date': get_today(),
        'day': 'A2 Day'
    }

    print(render_template('index.html', replacements))

main()
