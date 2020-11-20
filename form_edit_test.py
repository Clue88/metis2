# Copyright (c) 2020 Christopher Liu

#! /usr/bin/python3
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from date import format_date
from config import *
from templates import redirect
import pandas as pd
from sqlalchemy import create_engine

def main():
    form = cgi.FieldStorage()
    
    engine = create_engine('sqlite:///data/' + TEST_DB, echo=False)
    db = pd.read_sql('data/' + TEST_DB, con=engine, index_col='test_id')
    test_id = form.getvalue('test_id')
    
    db.loc[test_id, 'subject'] = form.getvalue('subject')
    db.loc[test_id, 'test'] = form.getvalue('test')
    db.loc[test_id, 'due'] = format_date(form.getvalue('due'))

    db.to_sql('data/' + TEST_DB, con=engine, if_exists='replace')

    print(redirect('index.py'))

main()
