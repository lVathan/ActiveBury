
from flask import Flask
from flask import request
from flask import render_template
from flask import session, redirect,url_for, flash, jsonify
from datetime import datetime
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.urls import url_parse

import sys
import os.path
import json

from flask_login import current_user, login_user, logout_user
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required




from app import app
from app import db
from app.weather import *
from app.events_calendar import *
from app.forms import LoginForm, RegistrationForm
from app.models import User

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/')
@app.route('/index')

def index():
    user = {'username': 'Nathan'}
    posts = [
        {
            'author': {'username': 'Bill'},
            'body': 'Beatiful Day!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)

@app.route('/login', methods =['GET', 'POST'])
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
        if not next_page or url_partse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<name>')
def user(name):

    user_agent = request.headers.get('User-Agent')
    return render_template('user.html', name=name, user_agent=user_agent)

@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/weather')
def weather():
    weather = current_weather(4373554)
    hour_forecast = hourly_forecast(4373554)
    five_forecast = five_day_forecast(4373554)

    return render_template('weather.html', weather=weather, hour_forecast=hour_forecast, five_forecast=five_forecast)

@app.route('/get_events')
def get_events():
    events=event_reader()
    return events

@app.route('/event_data')
def return_events():
    events=event_reader()
    return jsonify(events)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/calendar2')
def calendar2():
    events = get_events()
    return render_template('calendar.html', events=events)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500
