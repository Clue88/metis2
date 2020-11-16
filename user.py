import pandas as pd
from sqlalchemy import create_engine
from config import *

engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
df = pd.read_sql('data/' + USERS_DB, con=engine, index_col='user_id')

def get_name(id):
    return df.loc[id]['name']

def get_email(id):
    return df.loc[id]['email']

def get_classes(id):
    out = ''
    classes = remove_duplicates(df.loc[id].values.tolist()[4::2])
    classes.remove('Free Period')
    for _class in classes:
        out += '<option>' + _class + '</option>'
    return out


def remove_duplicates(items):
    out = []
    for element in items:
        if element not in out:
            out.append(element)
    return out
