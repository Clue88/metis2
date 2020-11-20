# Copyright (c) 2020 Christopher Liu

#! /usr/bin/python3
print('Content-type: text/html\n')

import cgi, cgitb
cgitb.enable()

from config import *
from templates import redirect
from uuid import uuid4
from hashlib import sha3_224
import pandas as pd
from sqlalchemy import create_engine
from date import format_date
from auth import get_id

def main():
    form = cgi.FieldStorage()

    d = {
        'user_id': [get_id()],
        'test_id': [uuid4().hex],
        'subject': [form.getvalue('subject') or 'N/A'],
        'test': [form.getvalue('test') or 'N/A'],
        'due': [format_date(form.getvalue('due') or '2020-09-28')],
        'done': [False]
    }

    df = pd.DataFrame(data=d)
    engine = create_engine('sqlite:///data/' + TEST_DB, echo=False)
    df.to_sql('data/' + TEST_DB, con=engine, index_label='ID', if_exists='append')

    print(redirect('index.py'))

main()
