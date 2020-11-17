import pandas as pd
from sqlalchemy import create_engine
from config import *
from datetime import datetime
from date import unformat_date

engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
df = pd.read_sql('data/' + USERS_DB, con=engine, index_col='user_id')
hw_engine = create_engine('sqlite:///data/' + HW_DB, echo=False)
hw_df = pd.read_sql('data/' + HW_DB, con=hw_engine, index_col='user_id')

def get_name(id):
    return df.loc[id]['name']

def get_email(id):
    return df.loc[id]['email']

def get_classes(id):
    out = ''
    classes = remove_duplicates(df.loc[id].values.tolist()[4::2])
    if 'Free Period' in classes:
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

def sortFunc(row):
    date_string = row.due
    date_object = datetime.strptime(date_string, '%a %m/%d/%y')

    return (date_object - datetime(1970,1,1)).days

def get_hw(id):
    hw_template = '''
        <tr>
            <td>// class //</td>
            <td>// assignment //</td>
            <td>// due //</td>
            <td>// submit //</td>
            <td>
                <form method="GET" action="edit_hw.py">
                    <input type="hidden" name="id" value="// id //">
                    <button class="button is-small is-info is-light" type="submit"><i class="fas fa-pencil-alt"></i></button>
                </form>
            </td>
            <td>
                <form method="GET" action="complete_hw.py">
                    <input type="hidden" name="id" value="// id //">
                    <button class="button is-small is-success is-light" type="submit"><i class="fas fa-check"></i></button>
                </form>
            </td>
        </tr>
    '''

    entries = ''
    hw_rows = []

    if id not in hw_df.index.tolist():
        return ''

    is_outstanding = hw_df['done'] != True
    user_hw = hw_df[is_outstanding].loc[id]
    
    if type(user_hw) == pd.core.series.Series:
        if user_hw.done == False:
            hw_rows.append(user_hw)
    else:
        for row in user_hw.iterrows():
            if row[1].done == True:
                continue
            hw_rows.append(row[1])
            
    hw_rows.sort(key=sortFunc)

    for row in hw_rows:

        if row.link != '':
            submit = '<a href="' + row.link + '" target="_blank">' + row.submit + '</a>'
        else:
            submit = row.submit
        
        entry = hw_template.replace('// class //', row.subject)
        entry = entry.replace('// assignment //', row.assignment)
        entry = entry.replace('// due //', row.due)
        entry = entry.replace('// submit //', submit)
        entry = entry.replace('// id //', row.hw_id)
        
        entries += entry

    return entries

def get_hw_info(hw_id):
    hw = hw_df.loc[hw_df['hw_id'] == hw_id]
    info = {
        'old_subject': hw.loc[:,'subject'].tolist()[0],
        'old_assignment': hw.loc[:,'assignment'].tolist()[0],
        'old_due': unformat_date(hw.loc[:,'due'].tolist()[0]),
        'old_submit': hw.loc[:,'submit'].tolist()[0],
        'old_link': hw.loc[:,'link'].tolist()[0]
    }
    return info
