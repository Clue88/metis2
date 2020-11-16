#! /usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from templates import render_template
from user import get_classes
from auth import get_id

def main():
    replacements = {
        'classes': get_classes(get_id())
    }

    print(render_template('new_hw.html', replacements))

main()
