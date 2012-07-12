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

sollie = Site(name="Sollie",lat="45",lon="54")
kiwanda = Site(name="Kiwanda",lat="45",lon="54")
petersons = Site(name="Peterson's",lat="45",lon="54")

sites = [sollie,kiwanda,petersons]

print "Importing site list"
for site in sites:
    print "Saving",site
    site.save()


