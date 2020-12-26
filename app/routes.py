from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    schedule = [
        {
            'period': 1,
            'times': '9:10 AM - 10:05 AM',
            'subject': 'AP US History'
        },
        {
            'period': 2,
            'times': '10:15 AM - 11:10 AM',
            'subject': 'BC Calc'
        },
        {
            'period': 3,
            'times': '11:20 AM - 12:15 PM',
            'subject': 'BC Calc'
        },
        {
            'period': 4,
            'times': '12:25 PM - 1:20 PM',
            'subject': 'Free Period'
        },
        {
            'period': 5,
            'times': '1:30 PM - 2:25 PM',
            'subject': 'AP Spanish'
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered! Please log in here.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
