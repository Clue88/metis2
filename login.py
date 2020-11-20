# Copyright (c) 2020 Christopher Liu

#! /usr/bin/python3
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from templates import render_template

def main():
    form = cgi.FieldStorage()
    if (form.getvalue('login') == 'success'):
        print(render_template('login.html', {'msg': 'Success! You can log in now.'}))
    elif (form.getvalue('login') == 'failed'):
        print(render_template('login.html', {'msg': 'Login failed. Please check your email and password and try again.'}))
    else:
        print(render_template('login.html', {'msg': ''}))
    
main()
