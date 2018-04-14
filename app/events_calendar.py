import os
import json
from flask_moment import Moment
from flask import Flask, render_template, url_for, json
from app.models import Event
#from datetime import datetime
import datetime

def event_reader():
    events= [
    {
        'start':'2018-03-14 14:00:00','title': 'Valentines Day'
    },
    {
        'start':'2018-03-17','title': 'Dinner'
    },
    {
        'start':'2018-03-13','title': 'Sergio and Odair Concert'
    },
    ]
    events2 = Event.query.all()
    for e in events2:
        color="blue"
        event_date_time=datetime.datetime.combine(e.start_date,e.start_time)
        if e.category == "general":
            color = "lightgreen"
        elif e.category == "sport":
            color = "lightblue"
        elif e.category == "family":
            color = "lightyellow"
        elif e.category == "social":
            color = "lighcoral"
        elif e.category == "cultural":
            color = "lightsalmon"
        else:
            color="blue"

        events.append(dict({'start': str(event_date_time), 'title': e.title,
                'color': color, 'textColor': 'black', 'url':'/event/{}'.format(e.id)}))

    return events
