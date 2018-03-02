
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

from flask_login import current_user, login_user, logout_user, login_required
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
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.forms import EventForm
from app.models import User, Post, Event

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home Page', form=form,
                            posts=posts.items, next_url=next_url,
                            prev_url=prev_url)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                            next_url=next_url, prev_url=prev_url)

@app.route('/add_events', methods=['GET', 'POST'])
@login_required
def add_events():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data,
                description=form.description.data, start_time=form.start_time.data,
                end_time=form.end_time.data,
                address=form.address.data, zipcode=form.zipcode.data,
                creater=current_user)
        db.session.add(event)
        db.session.commit()
        flash('Your event has been added to the calendar')
        return redirect(url_for('calendar'))
    return render_template('add_events.html', title='Add Events', form=form)

@app.route('/event/<id>')
@login_required
def event(id):
    event = Event.query.filter_by(id=int(id)).first_or_404()
    return render_template('event.html', event=event)

@app.route('/edit_event/<id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):

    form = EventForm()
    event=Event.query.filter_by(id=int(id)).first_or_404()
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.address = form.address.data
        event.zipcode = form.zipcode.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('event', id=id))
    elif request.method =='GET':
        form.title.data = event.title
        form.description.data = event.description
        form.start_time.data = event.start_time
        form.end_time.data = event.end_time
        form.address.data = event.address
        form.zipcode.data = event.zipcode
    return render_template('edit_event.html', title='Edit Event', form=form)


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
        if not next_page or url_parse(next_page).netloc != '':
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

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                            next_url=next_url, prev_url=prev_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash ('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash ('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/weather')
def weather():
    weather = current_weather(4373554)
    hour_forecast = hourly_forecast(4373554)
    five_forecast = five_day_forecast(4373554)

    return render_template('weather.html', weather=weather, hour_forecast=hour_forecast, five_forecast=five_forecast)


@app.route('/event_data')
def return_events():
    events=event_reader()
    return jsonify(events)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500
