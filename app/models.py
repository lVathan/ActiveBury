from datetime import datetime
from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)

subscriptions = db.Table('subscriptions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    events = db.relationship('Event', backref='creater', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_search = db.Column(db.Integer, default=21804)
    subscribed = db.relationship('Event', secondary=subscriptions,

        backref = db.backref('subscribers', lazy='dynamic'),
        lazy='dynamic')

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')


    def __repr__(self):
        return 'User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id)\
            .count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def subscribe(self, event):
        if not self.is_subscribed(event):
            self.subscribed.append(event)

    def unsubscribe(self, event):
        if self.is_subscribed(event):
            self.subscribed.remove(event)

    def is_subscribed(self, event):
        return self.subscribed.filter(subscriptions.c.event_id == event.id)\
            .count() > 0

    def subscribed_events(self):
        return Event.query\
            .join(subscriptions, (subscriptions.c.event_id == Event.id))\
            .filter(subscriptions.c.user_id == self.id)\
            .filter(Event.start_date >= datetime.now())\
            .order_by(Event.start_date)

    def past_events(self):
        return Event.query\
            .join(subscriptions, (subscriptions.c.event_id == Event.id))\
            .filter(subscriptions.c.user_id == self.id)\
            .filter(Event.start_date < datetime.now())\
            .order_by(Event.start_date)



    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return '<Post {}'.format(self.body)

class Event(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(240))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(140))
    zipcode = db.Column(db.Integer)
    category = db.Column(db.String(64))
    posts = db.relationship('Post', backref='topic', lazy='dynamic')
    image_url = db.Column(db.String(140), default=None, nullable=True)
    image_filename = db.Column(db.String(140), default=None, nullable=True)

    def __repr__(self):
        return '<Event {}'.format(self.title)

    def subscriber_count(self):
        return self.subscribers.count()


    def delete_event(self, user):
        if user == self.creater:
            db.session.delete(self)
            db.session.commit()
