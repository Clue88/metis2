import os
import pandas as pd
from sqlalchemy import create_engine
from config import *

def check_login():
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE'].split('; ')
        engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
        df = pd.read_sql('data/' + USERS_DB, con=engine, index_col='user_id')

        id = ''
        for cookie in cookies:
            if cookie.split('=')[0] == 'token':
                id = cookie.split('=')[1]
        if id != '':
            return True
        else:
            return False
    else:
        return False

def get_id():
    id = ''
    cookies = os.environ['HTTP_COOKIE'].split('; ')
    for cookie in cookies:
            if cookie.split('=')[0] == 'token':
                id = cookie.split('=')[1]
    return id

def get_existing_emails():
    engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
    df = pd.read_sql('data/' + USERS_DB, con=engine, index_col='user_id')
    s = df.loc[:, 'email']
    return s.to_list()

def get_old_pass(id):
    engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
    df = pd.read_sql('data/' + USERS_DB, con=engine, index_col='user_id')
    return df.loc[id, 'password']
