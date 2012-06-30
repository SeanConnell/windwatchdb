#!/usr/bin/python
from urllib import *
import xml.etree.ElementTree as xml 
import sys
from datetime import date, timedelta
args_list = { 
'lat' : '38.99',
'lon' : '-77.01',
'product' : 'time-series',
'begin' : '2004-01-01T00:00:00',
'end' : '2016-06-25T00:00:00',
'Unit' : 'e',
'maxt' : 'maxt',
'mint' : 'mint',
'temp' : 'temp',
'wdir' : 'wdir',
'sky' : 'sky',
'wx' : 'wx',
'appt' : 'appt',
'wgust' : 'wgust',
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
xml.fromstring(weather)
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
for params in param_list:
    for wvars in params.getchildren():
        wtime = wvars.attrib['time-layout']
        wtype = wvars.find('name').text
        index = 0 # <- a good sign I'm not doing this properly 
        for wtslice in wvars.findall('value'):
            lk_dict[wtime][index][wtype] = wtslice.text 
            index += 1

#join data ranges into time ranges based on time key

#build into dict of dicts (using datetime as key for second dict)
#second dict has wind dir, wind amplitude, etc
#iterate over data and turn it into objects
#save objects
