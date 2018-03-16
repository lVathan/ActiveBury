
from app import app
from app import db
from app.weather import *
from app.events_calendar import *
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.forms import EventForm
from app.models import User, Post, Event

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User, 'Post':Post, 'Event':Event}
