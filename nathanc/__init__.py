from flask import Flask

from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


app = Flask(__name__)

filename = 'secret_key'
app.config['SECRET_KEY'] = open(filename, 'rb').read()


bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)


import nathanc.views
