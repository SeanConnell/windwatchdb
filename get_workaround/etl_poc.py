#!/usr/bin/python
from urllib import *
import xml.etree.ElementTree as xml 
import sys
from datetime import date, timedelta
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
#tlist = time_dict.keys()
#tlist.sort()
#for t in tlist:
#    print t,time_dict[t]
#save objects

