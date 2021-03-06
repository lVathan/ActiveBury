from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField, IntegerField, DateTimeField, SelectField, SelectMultipleField
from wtforms import widgets
#from wtforms.fields.html5 import DateField
from wtforms_components import DateTimeField, TimeField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired



from app.models import User
from app import images
from datetime import datetime

from uszipcode import ZipcodeSearchEngine

def validate_zipcode(form, field):
    with ZipcodeSearchEngine() as search:
        zip=search.by_zipcode(field.data)
    if zip.City == None:
        raise ValidationError('Field must be a US Zipcode')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators =[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

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
    hyperlink = StringField('Link', validators=[Length(min=1, max=240), Optional()])
    start_date = DateField('Start Date', format="%Y-%m-%d",
                default=datetime.today, validators=[DataRequired()])
    start_time = TimeField('Start Time', format="%H:%M",
                default=datetime.now, validators=[Optional()])
    end_date = DateField('End Date', format="%Y-%m-%d", validators=[Optional()])
    end_time = TimeField('End Time', format="%H:%M", validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired(), validate_zipcode])
    category = SelectField('Category', choices=[('general', 'General'),
        ('sport', 'Sports'), ('family', 'Family'), ('social', 'Social'),
        ('cultural', 'Cultural')], default='general')
    submit = SubmitField('Register')

class PhotoUploadForm(FlaskForm):
    event_photo = FileField('images', validators=[
            FileRequired(),
            FileAllowed(images, 'Images only!')
            ])
    submit = SubmitField('Upload')

class SearchForm(FlaskForm):
    zipcode = IntegerField('Zipcode', validators=[DataRequired(), validate_zipcode])
    distance = SelectField('Distance', choices=[('100', '100'), ('30', '30'),
        ('10', '10')], default='30')
    submit = SubmitField('Search')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AdvancedSearchForm(FlaskForm):
    zipcode = IntegerField('Zipcode', validators=[DataRequired(), validate_zipcode])
    distance = SelectField('Distance', choices=[('100', '100'), ('30', '30'),
        ('10', '10')], default='30')
    start_date = DateField('Start Date', format="%Y-%m-%d",
                default=datetime.today, validators=[DataRequired()])
    end_date = DateField('End Date', format="%Y-%m-%d", validators=[Optional()])
    category = MultiCheckboxField('Category', choices=[('general', 'General'),
        ('sport', 'Sports'), ('family', 'Family'), ('social', 'Social'),
        ('cultural', 'Cultural')], validators=[Optional()])
    submit = SubmitField('Search')
