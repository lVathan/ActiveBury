import os
import json
from flask_moment import Moment
from flask import Flask, render_template, url_for, json

def event_reader():
    events= [
    {
        'start':'2018-2-14 14:00:00','title': 'Valentines Day'
    },
    {
        'start':'2018-2-17','title': 'Dinner'
    },
    {
        'start':'2018-2-13','title': 'Sergio and Odair Concert'
    },
    ]

    return events
