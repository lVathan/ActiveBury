from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField, IntegerField, DateTimeField, SelectField
#from wtforms.fields.html5 import DateField
from wtforms_components import DateTimeField, TimeField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Optional
from app.models import User
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators =[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=1, max=240)])
    start_date = DateField('Start Date', format="%Y-%m-%d",
                default=datetime.today, validators=[DataRequired()])
    start_time = TimeField('Start Time', format="%H:%M",
                default=datetime.now, validators=[Optional()])
    end_date = DateField('End Date', format="%Y-%m-%d", validators=[Optional()])
    end_time = TimeField('End Time', format="%H:%M", validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    zipcode = IntegerField('Zipcode', validators=[Optional()])
    category = SelectField('Category', choices=[('General', 'general'),
        ('Sports', 'sport'), ('Family', 'family'), ('Social', 'social'),
        ('Cultural', 'cultural')])
    submit = SubmitField('Register')
