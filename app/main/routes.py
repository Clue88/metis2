from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import EditProfileForm, EditClassesForm
from app.models import User
import os
from datetime import datetime

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # now = datetime.now()
    now = datetime(2021, 1, 12)
    print(now.strftime('%m/%d/%Y'))

    start = 0
    end = -1
    schedule_day = ''
    with open(os.path.join(os.getcwd(), 'data/stuyfall20.csv')) as f:
        lines = f.read().split('\n')
        for line in lines:
            if line.split(',')[0] == now.strftime('%-m/%-d/%-y'):
                start = int(line.split(',')[2])
                end = int(line.split(',')[3])
                schedule_day = line.split(',')[1].lower()

    times = []
    with open(os.path.join(os.getcwd(), 'data/stuyfall20times.csv')) as f:
        times = f.read().split('\n')

    schedule = []
    for i in range(start, end+1):
        schedule_item = {
            'period': i,
            'times': times[i-1].split(',')[1] + ' - ' + times[i-1].split(',')[2],
            'subject': current_user['period_' + str(i) + schedule_day],
            'link': current_user['period_' + str(i) + schedule_day + '_zoom']
        }
        schedule.append(schedule_item)

    if end == -1: day = 'No school today!'
    else:
        day = 'Day ' + schedule_day.upper() + ' (' + str(start) + '-' + str(end) + ')'

    homeworks = [
        {
            'subject': 'AP US History',
            'name': 'Homework 5',
            'due': 'Mon 12/14/20',
            'submit': 'Google Classroom',
            'link': 'https://classroom.google.com/u/0/c/MTU5ODM1MDAwMjc5/m/MTg1MTYxOTc1OTg2/details'
        },
        {
            'subject': 'AP English',
            'name': 'Read a Book',
            'due': 'Tue 12/15/20',
            'submit': 'Google Classroom',
            'link': 'https://classroom.google.com/u/0/c/MTU5ODM1MDAwMjc5/m/MTg1MTYxOTc1OTg2/details'
        }
    ]
    tests = [
        {
            'subject': 'BC Calc',
            'name': 'Group Test',
            'due': 'Wed 12/16/20'
        }
    ]

    date = now.strftime('%A, %B %-d, %Y')
    
    return render_template(
        'index.html', title='Home', date=date, day=day, homeworks=homeworks,
        tests=tests, schedule=schedule)

@bp.route('/profile')
@login_required
def profile():
    periods = {}
    for i in range(1, 11):
        periods['Period ' + str(i) + ' (A)'] = 'period_' + str(i) + 'a'
        periods['Period ' + str(i) + ' Zoom (A)'] = 'period_' + str(i) + 'a_zoom'
        periods['Period ' + str(i) + ' (B)'] = 'period_' + str(i) + 'b'
        periods['Period ' + str(i) + ' Zoom (B)'] = 'period_' + str(i) + 'b_zoom'

    return render_template('profile.html', title='Profile', periods=periods)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template(
        'edit_profile.html', title='Edit Profile', form=form)

@bp.route('/edit_classes', methods=['GET', 'POST'])
@login_required
def edit_classes():
    form = EditClassesForm()
    periods = []
    for i in range(1, 11):
        periods.append('period_' + str(i) + 'a')
        periods.append('period_' + str(i) + 'a_zoom')
        periods.append('period_' + str(i) + 'b')
        periods.append('period_' + str(i) + 'b_zoom')

    if form.validate_on_submit():
        for field in periods:
            current_user[field] = form[field].data
            # If B Day info is None, replace with A Day info
            if form[field].data is None:
                if field.endswith('b') and form[field[:-1] + 'a'].data is not None:
                    current_user[field] = form[field[:-1] + 'a'].data
                if field.endswith('b_zoom') and form[field[:-6] + 'a_zoom'].data is not None:
                    current_user[field] = form[field[:-6] + 'a_zoom'].data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        for field in periods:
            if current_user[field] is not None:
                form[field].data = current_user[field]
    return render_template(
        'edit_classes.html', title='Edit Classes', periods=periods, form=form)
