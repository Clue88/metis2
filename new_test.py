# Copyright (c) 2020 Christopher Liu

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

    print(render_template('new_test.html', replacements))

main()
