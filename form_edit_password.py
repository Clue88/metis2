#! /usr/bin/python
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from auth import get_id
from config import *
from templates import redirect
from hashlib import sha3_224
import pandas as pd
from sqlalchemy import create_engine

def main():
    form = cgi.FieldStorage()

    engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
    db = pd.read_sql('data/' + USERS_DB, con=engine, index_col='user_id')
    
    db.loc[get_id(), 'password'] = sha3_224(form.getvalue('new_password').encode('utf-8')).hexdigest()

    db.to_sql('data/users.db', con=engine, if_exists='replace')

    print(redirect('index.py'))

main()
    