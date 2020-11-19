# Copyright (c) 2020 Christopher Liu

#! /usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from templates import render_template
from user import get_classes, get_hw_info
from auth import get_id
from config import *

def main():
    form = cgi.FieldStorage()
    hw_id = form.getvalue('id')

    replacements = {
        'classes': get_classes(get_id()),
        'hw_id': hw_id
    }
    replacements.update(get_hw_info(hw_id))

    print(render_template('edit_hw.html', replacements))

main()
