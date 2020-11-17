#! /usr/bin/python
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
    test_id = form.getvalue('id')
    
    db.loc[test_id, 'done'] = True

    db.to_sql('data/' + TEST_DB, con=engine, if_exists='replace')

    print(redirect('index.py'))

main()
