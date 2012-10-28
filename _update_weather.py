#!/usr/bin/python
from urllib import *
import xml.etree.ElementTree as xml 
import sys
from datetime import datetime 
import re

#Get windwatcher and django on the import path
sys.path.append('/home/sean/django/windwatcher')
from django.core.management import setup_environ
import settings
setup_environ(settings)
from icarus.models import *

"""Pulls weather for a specific site, and puts it into the site's WeatherWatchQueue"""
def update_weather(site):
    args_list = { 
    'lat' : str(site.lat),
    'lon' : str(site.lon),
    'product' : 'time-series',
    'begin' : '2012-07-01T00:00:00',
    'end' : '2016-06-25T00:00:00',
    'Unit' : 'e',
    #'maxt' : 'maxt',
    #'mint' : 'mint',
    'temp' : 'temp',
    'wspd' : 'wspd',
    'wdir' : 'wdir',
    'rh' : 'rh',
    'sky' : 'sky',
    'wx' : 'wx',
    'appt' : 'appt',
    #'wgust' : 'wgust',
    'Submit' : 'Submit' }
    soap_query = 'http://graphical.weather.gov/xml/SOAP_server/ndfdXMLclient.php?whichClient=NDFDgen'

    """Parses out relevant groups of time, returns them as a dict of datetime objects FIXME: figure out gmt offset stuff"""
    def parse_timestring(string):
        extract_dt = re.compile('(^.*)(..:..:..)-(..:..)$',re.IGNORECASE) 
        times = extract_dt.match(string) 
        forecast_dt = str(times.group(1)) + str(times.group(2))
        date_it_happens = str(times.group(1))
        date_it_happens = date_it_happens.replace('T','')
        forecast_dt = forecast_dt.replace('T',' ') 
        start_time = str(times.group(2))
        gmt_offset = str(times.group(3)) 
        date_it_happens = datetime.strptime(date_it_happens,"%Y-%m-%d")
        start_time = datetime.strptime(start_time,"%H:%M:%S")
        times = {'forecast_dt':forecast_dt,
                 'date_it_happens':date_it_happens,
                 'start_time':start_time,
                 'gmt_offset':gmt_offset}
        return times

    """Parses relevant information into a weather time slice"""
    def create_wtime_slice(time, data_dict):
        wtslice = WeatherTimeSlice()
        #wtslice.temperature = int(data_dict['temperature'])
        try:
            wtslice.wind_speed = int(data_dict['wind_speed'])
            wtslice.wind_direction = int(data_dict['wind_direction'])
            wtslice.start_time = datetime.strptime(time,'%H:%M:%S') 
        except KeyError:
            print "NOAA fucked up, left out some data. Ignoring and continuing"
        return wtslice

    """Parses out relevant information into models and saves them"""
    def create_day_of_weather(date):
        dofweat = DayOfWeather()
        dofweat.prediction_date = datetime.now()
        dofweat.date_it_happens = datetime.strptime(date,'%Y/%m/%d') 
        dofweat.max_temperature = -100 #fix later
        dofweat.min_temperature = -100 #this too
        return dofweat

    # build that get query to the soap server, fucking punt on doing soap directly
    for arg in args_list.keys():
        soap_query += '&' + arg + '=' + args_list[arg] 

    print "Executing: [" +  soap_query + "]"
    weather_f = urlopen(soap_query)
    weather = weather_f.read()
    weather_f.close()

    #parse out some weather data for saving into the django class for the ORM
    #collect time keys and date ranges into hash 
    wxml = xml.fromstring(weather)
    wxml = wxml.find('data')

    #build first level of dict
    tl_list = wxml.findall('time-layout')
    lk_dict = {}

    #put in time ranges into appropriate keys
    for tl in tl_list:
        tk = tl.find('layout-key').text
        lk_dict[tk] = []
        for svt in tl.findall('start-valid-time'):
            lk_dict[tk].append({'time' : svt.text})

    #get data for time ranges
    param_list = wxml.findall('parameters')
    for params in param_list:
        for wvars in params.getchildren():
            wtime = wvars.attrib['time-layout']
            #for some reason strip wasn't doing anything, hack'd
            wtype = wvars.find('name').text.lower().replace(' ','_').replace(',','')
            index = 0 # <- a good sign I'm not doing this properly 
            for wtslice in wvars.findall('value'):
                lk_dict[wtime][index][wtype] = wtslice.text 
                index += 1

    #join data ranges into time ranges based on time key
    time_dict = {} 
    for tl in tl_list:
        tk = tl.find('layout-key').text
        for tslice in lk_dict[tk]:
            time = tslice['time']
            time_dict[time] = {}
            for param in tslice.keys():
                if param != 'time':
                    time_dict[time][param] = tslice[param]

    #build up the stupid multidimensional dict. God I've been writing too much perl...
    day_data_dict = {}
    try:
        for day in time_dict.keys():
            daytime = parse_timestring(day)
            date = daytime['date_it_happens'].strftime('%Y/%m/%d')
            time = daytime['start_time'].strftime('%H:%M:%S')
            day_data_dict[date] = {}
        for day in time_dict.keys():
            daytime = parse_timestring(day)
            date = daytime['date_it_happens'].strftime('%Y/%m/%d')
            time = daytime['start_time'].strftime('%H:%M:%S')
            day_data_dict[date][time] = {}
            for data in time_dict[day].keys():
                day_data_dict[date][time][data] = time_dict[day][data]
    except KeyError:
        print "NOAA fucked up, missing data in this returned data... Ignoring this chunk"

    day_list = day_data_dict.keys()
    day_list.sort()
    for day in day_list:
        dow = create_day_of_weather(day)
        #find WWQ for the site
        wwq = WeatherWatchQueue.objects.get(relevant_site=site)
        dow.weather_stream = wwq
        dow.prediction_date = datetime.now()
        print "saving day of weather",dow
        dow.save()
        for wts in day_data_dict[day].keys():
            wslice = create_wtime_slice(wts,day_data_dict[day][wts])
            wslice.day_of_occurance = dow
            wslice.save()
