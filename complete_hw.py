# Copyright (c) 2020 Christopher Liu

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
    
    engine = create_engine('sqlite:///data/' + HW_DB, echo=False)
    db = pd.read_sql('data/' + HW_DB, con=engine, index_col='hw_id')
    hw_id = form.getvalue('id')
    
    db.loc[hw_id, 'done'] = True

    db.to_sql('data/' + HW_DB, con=engine, if_exists='replace')

    print(redirect('index.py'))

main()
