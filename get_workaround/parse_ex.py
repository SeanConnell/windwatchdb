#!/usr/bin/python
#new way 
import xml.etree.ElementTree as xml 
xml.fromstring(weather)
#collect time keys and date ranges into hash 
wxml = xml.fromstring(weather)
wxml = wxml.find('data')
#build first level of dict
tl_list = wxml.findall('time-layout')
#put in time ranges into appropriate keys
for tl in tl_list:
	tk = tl.find('layout-key').text
	lk_dict[tk] = {}
	for svt in tl.findall('start-valid-time'):
	       lk_dict[tk][svt.text] = {} 

#join data ranges into time ranges based on time key
param_list = wxml.findall('parameters')
for params in param_list:
    for wvars in params.getchildren():
        wtime = wvars.attrib['time-layout']
        wtype = wvars.find('name').text
        print wtime,wtype
        for wtslice in wvars.findall('value'):
            print wtslice.text

#build into dict of dicts (using datetime as key for second dict)
#second dict has wind dir, wind amplitude, etc
#iterate over data and turn it into objects
#save objects
