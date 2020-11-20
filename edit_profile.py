# Copyright (c) 2020 Christopher Liu

#! /usr/bin/python3
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from templates import render_template
from config import *
from auth import get_id, get_old_pass
from user import get_name, get_email

def main():
    replacements = {
        'old_name': get_name(get_id()),
        'old_pass': get_old_pass(get_id())
    }
    
    print(render_template('edit_profile.html', replacements))

main()
