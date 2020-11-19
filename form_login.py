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
from auth import get_existing_emails

def main():
    form = cgi.FieldStorage()
    
    engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
    df = pd.read_sql('data/' + USERS_DB, con=engine, index_col='email')
    hashed = form.getvalue('password_hash') or ''

    if form.getvalue('email') in get_existing_emails():
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
    else:
        print(redirect('login.py?login=failed'))

main()
