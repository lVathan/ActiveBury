
from flask import Flask
from flask import request
from flask import render_template
from flask import session, redirect,url_for, flash, jsonify
from datetime import datetime
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import urllib.request
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
from app import images
from app.weather import *
from app.events_calendar import *
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, PhotoUploadForm, PasswordChangeForm, SearchForm
from app.forms import EventForm
from app.models import User, Post, Event

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    zipcode=21804
    distance=100
    if current_user.is_authenticated:
        zipcode=current_user.last_search
    form = SearchForm()
    if form.validate_on_submit():
        zipcode=form.zipcode.data
        distance=form.distance.data
        current_user.last_search = zipcode
        db.session.commit()
    elif request.method =='GET':
        form.zipcode.data = zipcode
        form.distance.data = distance
    zip = zip_info(zipcode)
    print(distance)
    events=[]
    events = day_event_reader(zipcode, distance)
    week_general_events=events[0]
    week_sport_events=events[1]
    week_family_events=events[2]
    week_social_events=events[3]
    week_cultural_events=events[4]
    days=events[5]
    day_count=[]



    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).\
        paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html',
                            zip=zip,
                            general_events = week_general_events,
                            sport_events = week_sport_events,
                            family_events = week_family_events,
                            social_events = week_social_events,
                            cultural_events = week_cultural_events,
                            posts=posts.items,
                            next_url=next_url,
                            days=days,
                            prev_url=prev_url,
                            day_count=range(5),
                            form=form)

@app.route('/add_events', methods=['GET', 'POST'])
@login_required
def add_events():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data,
                description=form.description.data,
                start_date=form.start_date.data,
                start_time=form.start_time.data,
                end_date=form.end_date.data,
                end_time=form.end_time.data,
                address=form.address.data,
                zipcode=form.zipcode.data,
                category=form.category.data,
                creater=current_user)
        db.session.add(event)
        current_user.subscribe(event)
        db.session.commit()
        flash('Your event has been added to the calendar')
        return redirect(url_for('index'))
    return render_template('add_events.html', title='Add Events', form=form)

@app.route('/event/<id>', methods=['GET', 'POST'])
def event(id):
    user = current_user
    form = PostForm()
    event = Event.query.filter_by(id=int(id)).first_or_404()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user, topic=event)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live')
        return redirect(url_for('event', id=id))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.topic_id==int(id)).order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('event.html', form=form, event=event, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/edit_event/<id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    form = EventForm()
    event=Event.query.filter_by(id=int(id)).first_or_404()
    if form.validate_on_submit() and event.creater==current_user:
        event.title = form.title.data
        event.description=form.description.data
        event.start_date=form.start_date.data
        if form.start_time.data:
            event.start_time=form.start_time.data
        if form.end_date.data:
            event.end_date=form.end_date.data
        if form.end_time.data:
            event.end_time=form.end_time.data
        if form.address.data:
            event.address=form.address.data
        if form.zipcode.data:
            event.zipcode=form.zipcode.data
        if form.category.data:
            event.category=form.category.data
        print(event.id)
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('event', id=id))
    elif request.method =='GET':
        form.title.data = event.title
        form.description.data = event.description
        form.start_date.data = event.start_date
        form.start_time.data = event.start_time
        form.end_date.data = event.start_date
        form.end_time.data = event.end_time
        form.address.data = event.address
        form.zipcode.data = event.zipcode
        form.category.data = event.category
    else:
        return redirect(url_for('event', id=id))

    return render_template('add_events.html', title='Edit Event', form=form)


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

@app.route('/password_change', methods=['GET', 'POST'])
@login_required
def password_change():
    user = current_user
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if user is None or not user.check_password(form.current_password.data):
            flash('Invalid username or password')
            return redirect(url_for('password_change'))
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password updated!')
        return redirect(url_for('index'))
    return(render_template('password_change.html', form=form))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    sub_events=user.subscribed_events().limit(7)
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                            events=sub_events,next_url=next_url,
                            prev_url=prev_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('user',username=current_user.username))
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

@app.route('/event/subscribe/<id>')
@login_required
def subscribe(id):
    event = Event.query.filter_by(id=id).first()
    if event is None:
        flash('Event not found.')
        return redirect(url_for('index'))
    if current_user.is_subscribed(event):
        flash('You are already subscribed')
        return redirect(url_for('event', id=id))
    current_user.subscribe(event)
    db.session.commit()
    flash('You are now subscribed to {}'.format(event.title))
    return redirect(url_for('event', id=id))

@app.route('/event/unsubscribe/<id>')
@login_required
def unsubscribe(id):
    event = Event.query.filter_by(id=id).first()
    if event is None:
        flash('Event not found.')
        return redirect(url_for('index'))
    if not current_user.is_subscribed(event):
        flash('You are already unsubscribed')
        return redirect(url_for('event', id=id))
    current_user.unsubscribe(event)
    db.session.commit()
    flash('You are now unsubscribed to {}'.format(event.title))
    return redirect(url_for('event', id=id))


@app.route('/event_data')
def return_events():
    events=event_reader(21804,30)
    return jsonify(events)


@app.route('/event_data/<zipcode>/<radius>')
def return_events_radius(zipcode, radius):
    events=event_reader(zipcode,radius)
    return jsonify(events)


@app.route('/calendar', methods = ['GET', 'POST'])
def calendar():
    zipcode=21804
    distance=100
    if current_user.is_authenticated:
        zipcode=current_user.last_search
    form = SearchForm()
    if form.validate_on_submit():
        zipcode=form.zipcode.data
        distance=form.distance.data
        current_user.last_search=zipcode
        db.session.commit()
    elif request.method =='GET':
        form.zipcode.data = zipcode
        form.distance.data = distance
    print(zipcode)
    return render_template('calendar.html', form=form, zipcode=zipcode, distance=distance)

@app.route('/upload/<id>', methods = ['GET', 'POST'])
@login_required
def upload(id):
    event=Event.query.filter_by(id=int(id)).first_or_404()
    form = PhotoUploadForm()
    if form.validate_on_submit():
        name_path='event/eventphoto_{}.'.format(event.id)

        f = form.event_photo.data
        filename = images.save(request.files['event_photo'],
                name=name_path)
        event.image_url=images.url(filename)
        db.session.commit()
        return redirect(url_for('event', id=id))
    return render_template('upload.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500
