#! /usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from config import *
from templates import redirect
from hashlib import sha3_224
import pandas as pd
from sqlalchemy import create_engine
import os

def main():
    form = cgi.FieldStorage()
    
    engine = create_engine('sqlite:///data/users.db', echo=False)
    df = pd.read_sql('data/users.db', con=engine, index_col='email')
    hashed = sha3_224(form.getvalue('password').encode('utf-8')).hexdigest()
    if df.loc[form.getvalue('email')]['password'] == hashed:
        cookie = '''
            <script>
                function setCookie(cname, cvalue, exdays) {
                    var d = new Date();
                    d.setTime(d.getTime() + (exdays*24*60*60*1000));
                    var expires = "expires="+ d.toUTCString();
                    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
                }

                setCookie("token", "//id//", 365);
            </script>
        '''
        cookie = cookie.replace('//id//', df.loc[form.getvalue('email')]['user_id'])
        print(cookie)
        print(redirect('index.py'))
    else:
        print(redirect('login.py?login=failed'))

main()
