# Startup helper functions

import sys

'''If your webserver is the PythonWebServer, then
1. you should have the StuyTools.py file in the same directory as your Python file
2. the top of your code should look like:

#! /usr/bin/python3

import StuyTools
StuyTools.PWS_startup()

'''

# Force the PythonWebServer to change to the directory containing the user's Python file
def PWS_startup():
    import os
    prog = sys.argv[0]
    # search for the last directory separator before the filename
    last_sep = prog.rfind('/')
    if last_sep < 0:
        last_sep = prog.rfind('\\')
    if last_sep < 0:
        return False
    # Change to that directory
    os.chdir(prog[:last_sep])
    return True


''' The Get_namevalues() function provides a uniform way to test your code, whether it's called
by the webserver (with name=value pairs derived from cgi.FieldStorage())
or on the command-line (with arguments as in:
     $fred.py  gpa=95.3  size=12  name=value ...)
or by providing a dictionary to your main() function like (all names and values must be strings):
    main({'gpa':'95.3', 'size':'12', 'name':'Fred'})
    

Use it by defining your main() function like...

def main(nv=StuyTools.Get_namevalues()):

... and inside main(), getting the incoming data with "nv.get(keyvalue,default_value)"

'''
def Get_namevalues():
    import cgi
    result = {}
    
    # if called by the webserver:
    form = cgi.FieldStorage()
    if len(form) > 0:
        for key in form.keys():
            result[key] = form.getvalue(key,'')
    
    # if called on the command-line
    elif len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            namevalue = arg.split('=')
            if len(namevalue) == 2:
                result[namevalue[0]] = namevalue[1]

    return result
