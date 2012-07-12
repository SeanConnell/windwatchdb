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

sollie = Site(name="Sollie",lat=45.476624,lon=-123.787594)
kiwanda = Site(name="Kiwanda",lat="45.224007",lon="-123.97316")
petersons = Site(name="Peterson's",lat=44.441134,lon=-123.013916)

sites = [sollie,kiwanda,petersons]

print "Importing site list"
for site in sites:
    print "Saving",site
    site.save()

#Create WWQs here after Sites have IDs
wwq1 = WeatherWatchQueue(relevant_site=sollie)
wwq2 = WeatherWatchQueue(relevant_site=kiwanda)
wwq3 = WeatherWatchQueue(relevant_site=petersons)
wwqs = [wwq1,wwq2,wwq3]

for wwq in wwqs:
    wwq.save()


