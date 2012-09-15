#!/usr/bin/python
import sys
from datetime import date, timedelta
from datetime import datetime 
import re

#Get windwatcher and django on the import path
#Fix this later
import getpass
user = getpass.getuser()
spath = "/home/" +  user + "/windwatchdb/django/windwatcher"
sys.path.append(spath)
from django.core.management import setup_environ
import settings
setup_environ(settings)
from icarus.models import *

testsite1 = Site(name="Test Site One",lat=45.476624,lon=-123.787594,city="Testcity",state="TestState")
testsite2 = Site(name="Test Site Two",lat=45.476624,lon=-123.787594,city="Testtowne",state="TestState")
site_list = [testsite1,testsite2]

print "Importing site list"
for site in site_list:
    site.save()
    print "Saving",site

testlaunchone = Launch(name="Test Launch One",site=testsite1,flyable_wind_speed_min=1,flyable_wind_speed_max=25,flyable_wind_direction_min=40,flyable_wind_direction_max=330)
testlaunchtwo = Launch(name="Test Launch Two",site=testsite2,flyable_wind_speed_min=9,flyable_wind_speed_max=15,flyable_wind_direction_min=140,flyable_wind_direction_max=330)
launch_list = [testlaunchone,testlaunchtwo]
for launch in launch_list:
    launch.save()
    print "Saving",launch

testlandingone = Landing(name="Test Landing One",site=testsite1,flyable_wind_speed_min=4,flyable_wind_speed_max=19,flyable_wind_direction_min=100,flyable_wind_direction_max=350)
testlandingtwo = Landing(name="Test Landing Two",site=testsite2,flyable_wind_speed_min=7,flyable_wind_speed_max=15,flyable_wind_direction_min=10,flyable_wind_direction_max=250)
landing_list = [testlandingone,testlandingtwo]

for landing in landing_list:
    landing.save()
    print "Saving",landing

#Create WWQs here after Sites have IDs
testwwq1 = WeatherWatchQueue(relevant_site=testsite1)
testwwq2 = WeatherWatchQueue(relevant_site=testsite2)
wwq_list = [testwwq1,testwwq2]

for wwq in wwq_list:
    wwq.save()
    print "Saving",wwq
