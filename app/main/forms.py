from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, Length
from app.models import User
from datetime import datetime

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Save')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')

class EditClassesForm(FlaskForm):
    period_1a = StringField('Period 1 (A)', validators=[Length(max=256)])
    period_1a_zoom = StringField('Period 1 Zoom (A)', validators=[Length(max=256)])
    period_1b = StringField('Period 1 (B)', validators=[Length(max=256)])
    period_1b_zoom = StringField('Period 1 Zoom (B)', validators=[Length(max=256)])

    period_2a = StringField('Period 2 (A)', validators=[Length(max=256)])
    period_2a_zoom = StringField('Period 2 Zoom (A)', validators=[Length(max=256)])
    period_2b = StringField('Period 2 (B)', validators=[Length(max=256)])
    period_2b_zoom = StringField('Period 2 Zoom (B)', validators=[Length(max=256)])

    period_3a = StringField('Period 3 (A)', validators=[Length(max=256)])
    period_3a_zoom = StringField('Period 3 Zoom (A)', validators=[Length(max=256)])
    period_3b = StringField('Period 3 (B)', validators=[Length(max=256)])
    period_3b_zoom = StringField('Period 3 Zoom (B)', validators=[Length(max=256)])

    period_4a = StringField('Period 4 (A)', validators=[Length(max=256)])
    period_4a_zoom = StringField('Period 4 Zoom (A)', validators=[Length(max=256)])
    period_4b = StringField('Period 4 (B)', validators=[Length(max=256)])
    period_4b_zoom = StringField('Period 4 Zoom (B)', validators=[Length(max=256)])

    period_5a = StringField('Period 5 (A)', validators=[Length(max=256)])
    period_5a_zoom = StringField('Period 5 Zoom (A)', validators=[Length(max=256)])
    period_5b = StringField('Period 5 (B)', validators=[Length(max=256)])
    period_5b_zoom = StringField('Period 5 Zoom (B)', validators=[Length(max=256)])

    period_6a = StringField('Period 6 (A)', validators=[Length(max=256)])
    period_6a_zoom = StringField('Period 6 Zoom (A)', validators=[Length(max=256)])
    period_6b = StringField('Period 6 (B)', validators=[Length(max=256)])
    period_6b_zoom = StringField('Period 6 Zoom (B)', validators=[Length(max=256)])

    period_7a = StringField('Period 7 (A)', validators=[Length(max=256)])
    period_7a_zoom = StringField('Period 7 Zoom (A)', validators=[Length(max=256)])
    period_7b = StringField('Period 7 (B)', validators=[Length(max=256)])
    period_7b_zoom = StringField('Period 7 Zoom (B)', validators=[Length(max=256)])

    period_8a = StringField('Period 8 (A)', validators=[Length(max=256)])
    period_8a_zoom = StringField('Period 8 Zoom (A)', validators=[Length(max=256)])
    period_8b = StringField('Period 8 (B)', validators=[Length(max=256)])
    period_8b_zoom = StringField('Period 8 Zoom (B)', validators=[Length(max=256)])

    period_9a = StringField('Period 9 (A)', validators=[Length(max=256)])
    period_9a_zoom = StringField('Period 9 Zoom (A)', validators=[Length(max=256)])
    period_9b = StringField('Period 9 (B)', validators=[Length(max=256)])
    period_9b_zoom = StringField('Period 9 Zoom (B)', validators=[Length(max=256)])

    period_10a = StringField('Period 10 (A)', validators=[Length(max=256)])
    period_10a_zoom = StringField('Period 10 Zoom (A)', validators=[Length(max=256)])
    period_10b = StringField('Period 10 (B)', validators=[Length(max=256)])
    period_10b_zoom = StringField('Period 10 Zoom (B)', validators=[Length(max=256)])

    submit = SubmitField('Save')

class NewHomeworkForm(FlaskForm):
    subject = SelectField('Subject', choices=[], validate_choice=False,
        validators=[DataRequired(), Length(max=64)])
    name = StringField('Assignment Name', validators=[DataRequired(), Length(max=64)])
    # Due Date needs to be a StringField to allow for no date (empty string
    # is not a valid date format)
    due_date = StringField('Due Date')
    submit_method = StringField('Submission Method', validators=[Length(max=64)])
    link = StringField('Assignment Link', validators=[Length(max=512)])
    submit = SubmitField('Add New Homework')

    def validate_due_date(self, due_date):
        try:
            datetime.strptime(due_date.data, '%Y-%m-%d')
        except:
            if due_date.data != '' and due_date.data is not None: raise ValidationError(
                'Please use the datepicker to enter a valid date.')

class EditHomeworkForm(FlaskForm):
    subject = SelectField('Subject', choices=[], validate_choice=False,
        validators=[DataRequired(), Length(max=64)])
    name = StringField('Assignment Name', validators=[DataRequired(), Length(max=64)])
    # Due Date needs to be a StringField to allow for no date (empty string
    # is not a valid date format)
    due_date = StringField('Due Date')
    submit_method = StringField('Submission Method', validators=[Length(max=64)])
    link = StringField('Assignment Link', validators=[Length(max=512)])
    submit = SubmitField('Save Homework')

    def validate_due_date(self, due_date):
        try:
            datetime.strptime(due_date.data, '%Y-%m-%d')
        except:
            if due_date.data != '' and due_date.data is not None: raise ValidationError(
                'Please use the datepicker to enter a valid date.')

class NewTestForm(FlaskForm):
    subject = SelectField('Subject', choices=[], validate_choice=False,
        validators=[DataRequired(), Length(max=64)])
    name = StringField('Assignment Name', validators=[DataRequired(), Length(max=64)])
    # Due Date needs to be a StringField to allow for no date (empty string
    # is not a valid date format)
    due_date = StringField('Due Date')
    submit = SubmitField('Add New Test')

    def validate_due_date(self, due_date):
        try:
            datetime.strptime(due_date.data, '%Y-%m-%d')
        except:
            if due_date.data != '' and due_date.data is not None: raise ValidationError(
                'Please use the datepicker to enter a valid date.')

class EditTestForm(FlaskForm):
    subject = SelectField('Subject', choices=[], validate_choice=False,
        validators=[DataRequired(), Length(max=64)])
    name = StringField('Assignment Name', validators=[DataRequired(), Length(max=64)])
    # Due Date needs to be a StringField to allow for no date (empty string
    # is not a valid date format)
    due_date = StringField('Due Date')
    submit = SubmitField('Save Test')

    def validate_due_date(self, due_date):
        try:
            datetime.strptime(due_date.data, '%Y-%m-%d')
        except:
            if due_date.data != '' and due_date.data is not None: raise ValidationError(
                'Please use the datepicker to enter a valid date.')

class CustomizationForm(FlaskForm):
    theme = SelectField('Theme', choices=['Default', 'Light'],
        validators=[DataRequired()])
    submit = SubmitField('Save')
