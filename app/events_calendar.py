import os
import json
from flask_moment import Moment
from flask import Flask, render_template, url_for, json
from app.models import Event

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
    events2 = Event.query.all()
    for e in events2:
        events.append(dict({'start': str(e.start_time), 'title': e.title, 'url':'/event/{}'.format(e.id)}))

 #session['cart'].append(dict({'product_id': id, 'qty': int(qty)}))

    return events
