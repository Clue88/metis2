from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    period_1a = db.Column(db.String(256))
    period_1a_zoom = db.Column(db.String(256))
    period_1b = db.Column(db.String(256))
    period_1b_zoom = db.Column(db.String(256))

    period_2a = db.Column(db.String(256))
    period_2a_zoom = db.Column(db.String(256))
    period_2b = db.Column(db.String(256))
    period_2b_zoom = db.Column(db.String(256))

    period_3a = db.Column(db.String(256))
    period_3a_zoom = db.Column(db.String(256))
    period_3b = db.Column(db.String(256))
    period_3b_zoom = db.Column(db.String(256))

    period_4a = db.Column(db.String(256))
    period_4a_zoom = db.Column(db.String(256))
    period_4b = db.Column(db.String(256))
    period_4b_zoom = db.Column(db.String(256))

    period_5a = db.Column(db.String(256))
    period_5a_zoom = db.Column(db.String(256))
    period_5b = db.Column(db.String(256))
    period_5b_zoom = db.Column(db.String(256))

    period_6a = db.Column(db.String(256))
    period_6a_zoom = db.Column(db.String(256))
    period_6b = db.Column(db.String(256))
    period_6b_zoom = db.Column(db.String(256))

    period_7a = db.Column(db.String(256))
    period_7a_zoom = db.Column(db.String(256))
    period_7b = db.Column(db.String(256))
    period_7b_zoom = db.Column(db.String(256))

    period_8a = db.Column(db.String(256))
    period_8a_zoom = db.Column(db.String(256))
    period_8b = db.Column(db.String(256))
    period_8b_zoom = db.Column(db.String(256))

    period_9a = db.Column(db.String(256))
    period_9a_zoom = db.Column(db.String(256))
    period_9b = db.Column(db.String(256))
    period_9b_zoom = db.Column(db.String(256))

    period_10a = db.Column(db.String(256))
    period_10a_zoom = db.Column(db.String(256))
    period_10b = db.Column(db.String(256))
    period_10b_zoom = db.Column(db.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64))
    name = db.Column(db.String(64))
    due_date = db.Column(db.DateTime, index=True, default=datetime(2020, 9, 28))
    submit = db.Column(db.String(64))
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Homework {}>'.format(self.name)
