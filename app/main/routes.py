from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import EditProfileForm, EditClassesForm
from app.models import User

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    schedule = [
        {
            'period': 1,
            'times': '9:10 AM - 10:05 AM',
            'subject': current_user.period_6b
        },
        {
            'period': 2,
            'times': '10:15 AM - 11:10 AM',
            'subject': current_user.period_2a
        },
        {
            'period': 3,
            'times': '11:20 AM - 12:15 PM',
            'subject': current_user.period_3a
        },
        {
            'period': 4,
            'times': '12:25 PM - 1:20 PM',
            'subject': current_user.period_4a
        },
        {
            'period': 5,
            'times': '1:30 PM - 2:25 PM',
            'subject': current_user.period_5a
        }
    ]
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
    return render_template('index.html', title='Home', date='Monday, December 14, 2020', day='Day A (1-5)', homeworks=homeworks, tests=tests, schedule=schedule)

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
