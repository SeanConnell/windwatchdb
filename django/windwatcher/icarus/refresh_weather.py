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
from _update_weather import update_weather
from _delete_weather import delete_weather

site_list = Site.objects.all()
for site in site_list:
    print "Refreshing weather information for",site
    delete_weather(site)
    update_weather(site)
    site.last_weather_refresh = datetime.now()
    site.save()
