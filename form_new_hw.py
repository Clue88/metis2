#! /usr/bin/python
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
        'hw_id': [uuid4().hex],
        'subject': [form.getvalue('subject') or 'N/A'],
        'assignment': [form.getvalue('assignment') or 'N/A'],
        'due': [format_date(form.getvalue('due') or '2020-09-28')],
        'submit': [form.getvalue('submit') or 'N/A'],
        'link': [form.getvalue('link') or ''],
        'done': [False]
    }

    df = pd.DataFrame(data=d)
    engine = create_engine('sqlite:///data/' + HW_DB, echo=False)
    df.to_sql('data/' + HW_DB, con=engine, index_label='ID', if_exists='append')

    print(redirect('index.py'))

main()
