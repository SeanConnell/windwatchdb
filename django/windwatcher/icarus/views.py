#!/usr/bin/python
#for debugging uncomment and run in ipython

import sys
sys.path.append('/home/sean/windwatchdb/django/windwatcher/')
from django.core.management import setup_environ 
import settings 
setup_environ(settings) 


from django.http import HttpResponse
from django.template import Context, loader
from icarus.models import *
import datetime, time

def index(request):
    template = loader.get_template('icarus/index.html')
    site_list = Site.objects.all().order_by('name') 
    weather_list = DayOfWeather.objects.all().order_by('date_it_happens')
    flyable_dict = {}
    for site in site_list:
        for day in weather_list:
            print site.site_check(site,day)
    dt_utc = datetime.datetime.utcnow()
    # convert UTC to local time
    dt_local = dt_utc - datetime.timedelta(seconds=time.altzone)
    context = Context({
        #'launch_list': launch_list,
        #'launch_dict': launch_dict,
        #'landing_list': landing_list,
        #'launch_dict': launch_dict,
        'datetime': dt_local.strftime("%A the %d, %B %Y at %r"),
        'site_list':site_list,
        'weather_list':weather_list,
        })
    return HttpResponse(template.render(context))

def site_list(request):
    template = loader.get_template('icarus/site_list.html')
    site_list = Site.objects.all().order_by('name') 
    weather_list = DayOfWeather.objects.all().order_by('date_it_happens')
    dt_utc = datetime.datetime.utcnow()
    # convert UTC to local time
    dt_local = dt_utc - datetime.timedelta(seconds=time.altzone)
    context = Context({
        'datetime': dt_local.strftime("%A the %d, %B %Y at %r"),
        'site_list':site_list,
        'weather_list':weather_list,
        })
    return HttpResponse(template.render(context))

def site(request,site_id=None):
    template = loader.get_template('icarus/site.html')
    site = Site.objects.get(id=site_id)
    wwq = WeatherWatchQueue.objects.get(relevant_site=site)
    weather_list = DayOfWeather.objects.filter(weather_stream=wwq)
    context = Context({
        'weather_list':weather_list,
        'site':site,
        })
    return HttpResponse(template.render(context))

def weather_day(request,dofweat_id=None,site_id=None):
    template = loader.get_template('icarus/day_of_weather.html')
    dofweat = DayOfWeather.objects.get(id=dofweat_id)
    site = Site.objects.get(id=site_id)
    tslice_list = WeatherTimeSlice.objects.filter(day_of_occurance=dofweat)
    tslice_list.extra(order_by = ['-start_time'])
    context = Context({
        'dofweat':dofweat,
        'title':site.name,
        'site':site,
        'tslice_list':tslice_list,
        })
    return HttpResponse(template.render(context))

