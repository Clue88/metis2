import pandas as pd
from sqlalchemy import create_engine
from config import *

engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
df = pd.read_sql('data/' + USERS_DB, con=engine, index_col='user_id')

def get_name(id):
    return df.loc[id]['name']
