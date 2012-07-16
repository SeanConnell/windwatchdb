#!/usr/bin/python
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

sollie = Site(name="Sollie Smith",lat=45.476624,lon=-123.787594,city="Tillamook",state="Oregon")
kiwanda = Site(name="Cape Kiwanda",lat="45.224007",lon="-123.97316",city="Pacific City",state="Oregon")
petersons = Site(name="Peterson's Butte",lat=44.441134,lon=-123.013916,city="Corvallis",state="Oregon")
dog = Site(name="Dog Mountain",lat=46.471325,lon=-122.168312,city="Morton",state="Washington")
cape_lookout = Site(name="Cape Lookout",lat=45.342494,lon=-123.978653,city="Tillamook",state="Oregon")
oceanside = Site(name="Oceanside",lat=45.462057,lon=-123.969727,city="Oceanside",state="Oregon")

sites = [sollie,kiwanda,petersons,dog,cape_lookout,oceanside]

print "Importing site list"
for site in sites:
    print "Saving",site
    site.save()

#Create WWQs here after Sites have IDs
wwq1 = WeatherWatchQueue(relevant_site=sollie)
wwq2 = WeatherWatchQueue(relevant_site=kiwanda)
wwq3 = WeatherWatchQueue(relevant_site=petersons)
wwq4 = WeatherWatchQueue(relevant_site=dog)
wwq5 = WeatherWatchQueue(relevant_site=cape_lookout)
wwq6 = WeatherWatchQueue(relevant_site=oceanside)
wwqs = [wwq1,wwq2,wwq3,wwq4,wwq5,wwq6]

for wwq in wwqs:
    wwq.save()


