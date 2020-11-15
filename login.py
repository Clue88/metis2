#! /usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from templates import render_template

def main():
    form = cgi.FieldStorage()
    if (form.getvalue('login') == 'success'):
        print(render_template('login.html', {'msg': 'Success! You can log in now.'}))
    else:
        print(render_template('login.html', {'msg': ''}))
    

main()
