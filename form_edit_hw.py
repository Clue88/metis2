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
    hw_id = form.getvalue('hw_id')
    
    db.loc[hw_id, 'subject'] = form.getvalue('subject')
    db.loc[hw_id, 'assignment'] = form.getvalue('assignment')
    db.loc[hw_id, 'due'] = format_date(form.getvalue('due'))
    db.loc[hw_id, 'submit'] = form.getvalue('submit')
    db.loc[hw_id, 'link'] = form.getvalue('link')

    db.to_sql('data/' + HW_DB, con=engine, if_exists='replace')

    print(redirect('index.py'))

main()
