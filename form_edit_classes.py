# Copyright (c) 2020 Christopher Liu

#! /usr/bin/python3
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from auth import get_id
from config import *
from templates import redirect
import pandas as pd
from sqlalchemy import create_engine

def main():
    form = cgi.FieldStorage()

    engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
    db = pd.read_sql('data/' + USERS_DB, con=engine, index_col='user_id')

    for i in range(1, NUM_PERIODS+1):
        db.loc[get_id(), 'p'+str(i)+'a'] = form.getvalue('p'+str(i)+'a')
        db.loc[get_id(), 'p'+str(i)+'za'] = form.getvalue('p'+str(i)+'za') or ''
        db.loc[get_id(), 'p'+str(i)+'b'] = form.getvalue('p'+str(i)+'b') or form.getvalue('p'+str(i)+'a')
        db.loc[get_id(), 'p'+str(i)+'zb'] = form.getvalue('p'+str(i)+'zb') or form.getvalue('p'+str(i)+'za') or ''

    db.to_sql('data/users.db', con=engine, if_exists='replace')

    print(redirect('index.py'))

main()
    