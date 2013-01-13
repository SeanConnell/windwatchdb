#!/usr/bin/python
from urllib import *
import sys
from datetime import datetime 
import getpass
user = getpass.getuser()
#Get windwatcher and django on the import path

spath = "/home/" +  user + "/windwatchdb/django/windwatcher"
sys.path.append(spath)
from django.core.management import setup_environ
import settings
setup_environ(settings)
from icarus.models import *
from _update_weather import update_weather
from _delete_weather import delete_weather
#from icarus.memoize import clear_cache


site_list = Site.objects.all()
for site in site_list:
    print "Updating Predictions for %s" % site
    print "Deleting previous Predictions"
    delete_weather(site)
    print "Getting new Weather Predictions"
    update_weather(site)
    site.last_weather_refresh = datetime.now()
    site.save()

#print "Clearing memoization caches"
#clear_cache()
