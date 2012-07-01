#!/usr/bin/python

from SOAPpy import *
import  xml.etree.ElementTree as etreeXml 
import sys
from datetime import date, timedelta

service_url ='http://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php'
namespace = 'http://graphical.weather.gov/xml/DWMLgen/wsdl/ndfdXML.wsdl#NDFDgenByDay'
client = SOAPProxy(service_url, namespace)
client.config.debug = 1
lat = stringType('38.99')
lat._name = 'latitude'
lon = stringType('-77.01')
lon._name = 'longitude'
product = stringType('time-series') #'glance' #other option is time-series, not sure which is what I want right now..
product._name = 'product'
start_time = dateTimeType([2012,6,12,20,32,32])
start_time._name = 'startTime' 
end_time = dateTimeType([2012,6,13,20,32,32])
end_time._name = 'endTime'
unit = stringType('e') #Use those horrible imperial units because everybody expects them...
unit._name = 'unit'
#List of what you want back
maxt = booleanType('true')
maxt._name = 'maxt'
mint = booleanType('true')
mint._name = 'mint'
wdir = booleanType('true')
wdir._name = 'wdir'
temp = booleanType('true')
temp._name = 'temp'
weather_params = structType(name='weatherParameters')
weather_params._addItem('maxt',maxt)
weather_params._addItem('mint',mint)
weather_params._addItem('wdir',wdir)
weather_params._addItem('temp',temp)
#weather_params = arrayType([maxt,mint,wdir,temp])
#weather_params._name = 'weatherParameters'
weather = client.NDFDgen(lat,lon,product,start_time,end_time,unit,weather_params)
#print weather
sys.exit(0)
#weather = etreeXml.XML(weather)
#w_metadata = weather.find('head')
#w_data = weather.find('data')
#print w_data
#start_time = date.today() - timedelta(1)#datetime object of start for prediction, use yesterday for now
#end_time = date.today().strftime("")#datetime of today with soap format of yyyymmddThhmmss
