#! /usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from templates import render_template
from user import get_classes, get_test_info
from auth import get_id
from config import *

def main():
    form = cgi.FieldStorage()
    test_id = form.getvalue('id')

    replacements = {
        'classes': get_classes(get_id()),
        'test_id': test_id
    }
    replacements = replacements|get_test_info(test_id)

    print(render_template('edit_test.html', replacements))

main()
