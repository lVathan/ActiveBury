import urllib.request
import json
import pyowm
import datetime

weather_api = '726c97f8af2670934a95bbccc6d4154c'
owm = pyowm.OWM(weather_api)

def weather_data(w):
    weather={}

    weather['time'] = w.get_reference_time(timeformat='date')

    weather['status'] = w.get_detailed_status()
    weather['temperature'] = w.get_temperature(unit='fahrenheit')
    weather['wind'] = w.get_wind()
    weather['pressure'] = w.get_pressure()
    weather['humidity'] = w.get_humidity()
    return weather



def five_day_forecast(num):
    num=num
    fc = owm.daily_forecast_at_id(num, limit=6)
    f = fc.get_forecast()
    list = f.get_weathers()
    forecast=[]
    for w in list:
        forecast.append(weather_data(w))
    return forecast

def hourly_forecast(num):
    fc = owm.three_hours_forecast_at_id(num)
    f = fc.get_forecast()
    list = f.get_weathers()
    forecast=[]
    for w in list:
        forecast.append(weather_data(w))
    return forecast[:8]

def current_weather(num):
    obs = owm.weather_at_id(num)
    w=obs.get_weather()
    data = weather_data(w)

    return data


def weather_search():
    key = weather_api
    url = 'http://api.openweathermap.org/data/2.5/forecast?id=4373554&APPID=' + key
    json_obj = urllib.request.urlopen(url)
    data = json.load(json_obj)
