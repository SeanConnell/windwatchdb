#!/usr/bin/python
from urllib import *
import xml.etree.ElementTree as xml 
import sys
from datetime import date, timedelta
from datetime import datetime 
import re

#Get windwatcher and django on the import path
sys.path.append('/home/sean/django/windwatcher')
from django.core.management import setup_environ
import settings
setup_environ(settings)
from icarus.models import *

args_list = { 
'lat' : '45.50',
'lon' : '-122.6',
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
def save_wtime_slice(times, data_dict, dofweat):
    wtslice = WeatherTimeSlice()
    wtslice.temperature = int(data_dict[time]['temperature'])
    wtslice.wind_speed = int(data_dict[time]['wind_speed'])
    wtslice.wind_direction = int(data_dict[time]['wind_direction'])
    wtslice.start_time = times['start_time']
    wtslice.day_of_occurance = dofweat
    print "saving slice of", wtslice
    wtslice.save()

"""Parses out relevant information into models and saves them"""
def save_day_of_weather(times, data_dict):
    #save objects
    dofweat = DayOfWeather()
    dofweat.prediction_date = datetime.now()
    dofweat.date_it_happens = times['date_it_happens'] 
    dofweat.max_temperature = -100 #fix later
    dofweat.min_temperature = -100 #this too
    print "saving day", dofweat
    dofweat.save()
    save_wtime_slice(times,data_dict,dofweat)

# build that get query to the soap server, fucking punt on doing soap directly
for arg in args_list.keys():
    soap_query += '&' + arg + '=' + args_list[arg] 

print "Executing: [" +  soap_query + "]"
#Yeah, urllib has some support for forms, but whatever, this works well
weather_f = urlopen(soap_query)
#get the data from the file like object
weather = weather_f.read()
#close the object like a good citizen
weather_f.close()
#parse out some weather data for saving into the django class for the ORM
#xml.fromstring(weather)
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

#debugging output:
tlist = time_dict.keys()
tlist.sort()
#fix this so I'm not overwriting the same day a whole bunch
for time in tlist:
    #print time,time_dict[time]
    times = parse_timestring(time)
    save_day_of_weather(times, time_dict)
