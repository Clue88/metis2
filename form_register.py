# Copyright (c) 2020 Christopher Liu

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

def main():
    form = cgi.FieldStorage()
    d = {
        'user_id': [uuid4().hex],
        'email': [form.getvalue('email')],
        'name': [form.getvalue('name')],
        'password': [form.getvalue('password_hash')],
        'p1a': form.getvalue('p1a'),
        'p1za': form.getvalue('p1za') or '',
        'p1b': form.getvalue('p1b') or form.getvalue('p1a'),
        'p1zb': form.getvalue('p1zb') or form.getvalue('p1za') or '',
        'p2a': form.getvalue('p2a'),
        'p2za': form.getvalue('p2za') or '',
        'p2b': form.getvalue('p2b') or form.getvalue('p2a'),
        'p2zb': form.getvalue('p2zb') or form.getvalue('p2za') or '',
        'p3a': form.getvalue('p3a'),
        'p3za': form.getvalue('p3za') or '',
        'p3b': form.getvalue('p3b') or form.getvalue('p3a'),
        'p3zb': form.getvalue('p3zb') or form.getvalue('p3za') or '',
        'p4a': form.getvalue('p4a'),
        'p4za': form.getvalue('p4za') or '',
        'p4b': form.getvalue('p4b') or form.getvalue('p4a'),
        'p4zb': form.getvalue('p4zb') or form.getvalue('p4za') or '',
        'p5a': form.getvalue('p5a'),
        'p5za': form.getvalue('p5za') or '',
        'p5b': form.getvalue('p5b') or form.getvalue('p5a'),
        'p5zb': form.getvalue('p5zb') or form.getvalue('p5za') or '',
        'p6a': form.getvalue('p6a'),
        'p6za': form.getvalue('p6za') or '',
        'p6b': form.getvalue('p6b') or form.getvalue('p6a'),
        'p6zb': form.getvalue('p6zb') or form.getvalue('p6za') or '',
        'p7a': form.getvalue('p7a'),
        'p7za': form.getvalue('p7za') or '',
        'p7b': form.getvalue('p7b') or form.getvalue('p7a'),
        'p7zb': form.getvalue('p7zb') or form.getvalue('p7za') or '',
        'p8a': form.getvalue('p8a'),
        'p8za': form.getvalue('p8za') or '',
        'p8b': form.getvalue('p8b') or form.getvalue('p8a'),
        'p8zb': form.getvalue('p8zb') or form.getvalue('p8za') or '',
        'p9a': form.getvalue('p9a'),
        'p9za': form.getvalue('p9za') or '',
        'p9b': form.getvalue('p9b') or form.getvalue('p9a'),
        'p9zb': form.getvalue('p9zb') or form.getvalue('p9za') or '',
        'p10a': form.getvalue('p10a'),
        'p10za': form.getvalue('p10za') or '',
        'p10b': form.getvalue('p10b') or form.getvalue('p10a'),
        'p10zb': form.getvalue('p10zb') or form.getvalue('p10za') or '',
    }

    df = pd.DataFrame(data=d)
    engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
    df.to_sql('data/' + USERS_DB, con=engine, index_label='ID', if_exists='append')

    print(redirect('login.py?login=success'))

main()
