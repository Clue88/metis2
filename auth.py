import os
import pandas as pd
from sqlalchemy import create_engine

def check_login():
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE'].split(';')
        engine = create_engine('sqlite:///data/users.db', echo=False)
        df = pd.read_sql('data/users.db', con=engine, index_col='user_id')

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
