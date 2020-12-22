from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Christopher'}
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
    return render_template('index.html', title='Home', date='Monday, December 14, 2020', day='Day A (1-5)', user=user, homeworks=homeworks, tests=tests, schedule=schedule)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Log In', form=form)
