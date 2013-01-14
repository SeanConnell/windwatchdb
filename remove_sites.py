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

site_list = Site.objects.all()
for site in site_list:
    print "Deleting site ", site
    site.delete()

#print "Clearing memoization caches"
#clear_cache()
