
from flask import Flask
from flask import request
from flask import render_template
from flask import session, redirect,url_for, flash
from datetime import datetime
from werkzeug.contrib.fixers import ProxyFix
import sys
import os.path

from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required




from nathanc import app
from nathanc.weather import *


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.datetime.utcnow(), form=form, name=session.get('name'))

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



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500
