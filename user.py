import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite:///data/users.db', echo=False)
df = pd.read_sql('data/users.db', con=engine, index_col='user_id')

def get_name(id):
    return df.loc[id]['name']
