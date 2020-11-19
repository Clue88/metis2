# Copyright (c) 2020 Christopher Liu

#! /usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from templates import render_template
from schedules import period_forms_edit, get_schedule_data
from config import *
from string import Template
from auth import get_id

def main():
    replacements = {
        'periods': period_forms_edit(NUM_PERIODS),
    }
    values = get_schedule_data(get_id())
    print(Template(render_template('edit_classes.html', replacements)).safe_substitute(values))

main()
