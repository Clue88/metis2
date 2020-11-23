# Copyright (c) 2020 Christopher Liu

import os
import pandas as pd
from sqlalchemy import create_engine
from config import *

engine = create_engine('sqlite:///data/' + USERS_DB, echo=False)
df = pd.read_sql('data/' + USERS_DB, con=engine, index_col='user_id')

def get_schedules(id, letter, start, end):
    schedule = ''
    class_template = '''
        <tr>
            <th>//period//</th>
            <td>//times//</td>
            <td><a href="//link//" target="_blank">//name//</a></td>
        </tr>
    '''
    for i in range(int(start), int(end)+1):
        _class = class_template
        _class = _class.replace('//period//', str(i))

        if (df.loc[id]['p'+str(i)+'z'+letter.lower()] != ''):
            _class = _class.replace('//link//', df.loc[id]['p'+str(i)+'z'+letter.lower()])
        else:
            _class = _class.replace('<td><a href="//link//" target="_blank">//name//</a></td>', '<td>//name//</td>')

        _class = _class.replace('//name//', df.loc[id]['p'+str(i)+letter.lower()])
        _class = _class.replace('//times//', get_times(i))
        schedule += _class
    return schedule

def get_times(period):
    f = open(os.path.join('data', SCHEDULE_TIMES))
    s = f.read()
    f.close()
    
    lines = s.split('\n')
    for line in lines:
        if line.split(',')[0] == str(period):
            return line.split(',')[1] + ' - ' + line.split(',')[2]
    return ''

def period_forms(num):
    out = ''
    period_template = '''
        <input class="input" type="text" name="p//pd//a" placeholder="Period //pd// Class Day A" value="Free Period">
        <p class="help" id=p//pd//a></p>
        <input class="input" type="text" name="p//pd//za" placeholder="Period //pd// Zoom Link Day A">
        <input class="input" type="text" name="p//pd//b" placeholder="Period //pd// Class Day B (if necessary)">
        <input class="input" type="text" name="p//pd//zb" placeholder="Period //pd// Zoom Link Day B (if necessary)">
        <br><br>
    '''
    for i in range(1, num+1):
        out += period_template.replace('//pd//', str(i))
    return out

def period_forms_edit(num):
    out = ''
    period_template = '''
        <input class="input" type="text" name="p//pd//a" placeholder="Period //pd// Class Day A" value="$p//pd//a">
        <p class="help" id=p//pd//a></p>
        <input class="input" type="text" name="p//pd//za" placeholder="Period //pd// Zoom Link Day A" value="$p//pd//za">
        <input class="input" type="text" name="p//pd//b" placeholder="Period //pd// Class Day B (if necessary)" value="$p//pd//b">
        <input class="input" type="text" name="p//pd//zb" placeholder="Period //pd// Zoom Link Day B (if necessary)" value="$p//pd//zb">
        <br><br>
    '''
    for i in range(1, num+1):
        out += period_template.replace('//pd//', str(i))
    return out

def get_schedule_data(id):
    return df.loc[id]
