from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
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
    period_1a = StringField('Period 1 (A)')
    period_1a_zoom = StringField('Period 1 Zoom (A)')
    period_1b = StringField('Period 1 (B)')
    period_1b_zoom = StringField('Period 1 Zoom (B)')

    period_2a = StringField('Period 2 (A)')
    period_2a_zoom = StringField('Period 2 Zoom (A)')
    period_2b = StringField('Period 2 (B)')
    period_2b_zoom = StringField('Period 2 Zoom (B)')

    period_3a = StringField('Period 3 (A)')
    period_3a_zoom = StringField('Period 3 Zoom (A)')
    period_3b = StringField('Period 3 (B)')
    period_3b_zoom = StringField('Period 3 Zoom (B)')

    period_4a = StringField('Period 4 (A)')
    period_4a_zoom = StringField('Period 4 Zoom (A)')
    period_4b = StringField('Period 4 (B)')
    period_4b_zoom = StringField('Period 4 Zoom (B)')

    period_5a = StringField('Period 5 (A)')
    period_5a_zoom = StringField('Period 5 Zoom (A)')
    period_5b = StringField('Period 5 (B)')
    period_5b_zoom = StringField('Period 5 Zoom (B)')

    period_6a = StringField('Period 6 (A)')
    period_6a_zoom = StringField('Period 6 Zoom (A)')
    period_6b = StringField('Period 6 (B)')
    period_6b_zoom = StringField('Period 6 Zoom (B)')

    period_7a = StringField('Period 7 (A)')
    period_7a_zoom = StringField('Period 7 Zoom (A)')
    period_7b = StringField('Period 7 (B)')
    period_7b_zoom = StringField('Period 7 Zoom (B)')

    period_8a = StringField('Period 8 (A)')
    period_8a_zoom = StringField('Period 8 Zoom (A)')
    period_8b = StringField('Period 8 (B)')
    period_8b_zoom = StringField('Period 8 Zoom (B)')

    period_9a = StringField('Period 9 (A)')
    period_9a_zoom = StringField('Period 9 Zoom (A)')
    period_9b = StringField('Period 9 (B)')
    period_9b_zoom = StringField('Period 9 Zoom (B)')

    period_10a = StringField('Period 10 (A)')
    period_10a_zoom = StringField('Period 10 Zoom (A)')
    period_10b = StringField('Period 10 (B)')
    period_10b_zoom = StringField('Period 10 Zoom (B)')

    submit = SubmitField('Save')

class NewHomeworkForm(FlaskForm):
    subject = SelectField('Subject', choices=[], validate_choice=False,
        validators=[DataRequired()])
    name = StringField('Assignment Name', validators=[DataRequired()])
    # Due Date needs to be a StringField to allow for no date (empty string
    # is not a valid date format)
    due_date = StringField('Due Date')
    submit_method = StringField('Submission Method')
    link = StringField('Assignment Link')
    submit = SubmitField('Add New Homework')
