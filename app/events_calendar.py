import os
import json
from flask_moment import Moment
from flask import Flask, render_template, url_for, json
from app.models import Event
#from datetime import datetime
import datetime
from uszipcode import ZipcodeSearchEngine



def zipsearch(zipcode, distance):
    with ZipcodeSearchEngine() as search:
        zip=search.by_zipcode(zipcode)
        searchlist=search.by_coordinate(zip.Latitude, zip.Longitude, radius=int(distance), returns=0)
        ziplist=[]
        for z in searchlist:
            ziplist.append(z.Zipcode)
        return list(map(int, ziplist))

def zip_info(zipcode):
    with ZipcodeSearchEngine() as search:
        zip=search.by_zipcode(zipcode)
    return [zip.City, zip.State]

def event_reader(zipcode, radius):
    events= []
    events2 = Event.query.all()
    zips = zipsearch(zipcode, radius)
    for e in events2:
        if e.zipcode in zips:
            color="blue"
            event_date_time=datetime.datetime.combine(e.start_date,e.start_time)
            if e.category == "general":
                color = "lightgreen"
            elif e.category == "sport":
                color = "lightblue"
            elif e.category == "family":
                color = "lightyellow"
            elif e.category == "social":
                color = "lightcoral"
            elif e.category == "cultural":
                color = "lightsalmon"
            else:
                color="blue"
            events.append(dict({'start': str(event_date_time), 'title': e.title,
                'color': color, 'textColor': 'black', 'url':'/event/{}'.format(e.id)}))
    return events

def advanced_search_reader(zipcode, radius, start_date, end_date, category, page):
    zips = zipsearch(zipcode, radius)
    return Event.query\
        .filter(Event.zipcode.in_(zips))\
        .filter(Event.start_date >= start_date)\
        .filter(Event.end_date <= end_date)\
        .filter(Event.category.in_(category))\
        .order_by(Event.start_date)\
        .paginate(page, 15, False)


def day_event_reader_2(zipcode, radius):
    zips = zipsearch(zipcode, radius)
    day1 =  Event.query\
        .filter(Event.zipcode.in_(zips))\
        .filter(Event.start_date >= datetime.datetime.now())\
        .filter(Event.start_date <= end_date)\
        .filter(Event.category.in_(category))\
        .order_by(Event.start_date)

def day_event_reader(zipcode, radius):
    days=[]
    next_days=[]
    week_general_events=[0,1,2,3,4,5]
    week_sport_events=[0,1,2,3,4,5]
    week_family_events=[0,1,2,3,4,5]
    week_social_events=[0,1,2,3,4,5]
    week_cultural_events=[0,1,2,3,4,5]

    week_general_events_local=[[],[],[],[],[]]
    week_sport_events_local=[[],[],[],[],[]]
    week_family_events_local=[[],[],[],[],[]]
    week_social_events_local=[[],[],[],[],[]]
    week_cultural_events_local=[[],[],[],[],[]]


    zips = zipsearch(zipcode, radius)

    for day in range(5):
        days.append(datetime.datetime.now()+datetime.timedelta(days=day))
        next_days.append(datetime.datetime.now()+datetime.timedelta(days=day+1))
        week_general_events[day]=Event.query\
                .filter(Event.start_date >= days[day].date(),\
                Event.start_date < next_days[day].date(),\
                 Event.category == 'general')\
                 .order_by(Event.start_time)\
                 .all()
        if week_general_events[day]:
            for ev in week_general_events[day]:
                if ev.zipcode in zips:
                    week_general_events_local[day].append(ev)


        week_sport_events[day]=Event.query.filter(Event.start_date >= days[day].date(),\
                Event.start_date < next_days[day].date(),\
                 Event.category == 'sport').order_by(Event.start_time).all()
        for ev in week_sport_events[day]:
            if ev.zipcode in zips:
                week_sport_events_local[day].append(ev)

        week_family_events[day]=Event.query.filter(Event.start_date >= days[day].date(),\
                Event.start_date < next_days[day].date(),\
                 Event.category == 'family').order_by(Event.start_time).all()
        for ev in week_family_events[day]:
            if ev.zipcode in zips:
                week_family_events_local[day].append(ev)

        week_social_events[day]=Event.query.filter(Event.start_date >= days[day].date(),\
                Event.start_date < next_days[day].date(),\
                 Event.category == 'social').order_by(Event.start_time).all()
        for ev in week_social_events[day]:
            if ev.zipcode in zips:
                week_social_events_local[day].append(ev)

        week_cultural_events[day]=Event.query.filter(Event.start_date >= days[day].date(),\
                Event.start_date < next_days[day].date(),\
                 Event.category == 'cultural').order_by(Event.start_time).all()
        for ev in week_cultural_events[day]:
            if ev.zipcode in zips:
                week_cultural_events_local[day].append(ev)

    return week_general_events_local,\
            week_sport_events_local,\
            week_family_events_local,\
            week_social_events_local,\
            week_cultural_events_local,\
            days
