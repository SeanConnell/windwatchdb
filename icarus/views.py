#!/usr/bin/python
#for debugging uncomment and run in ipython

import sys
sys.path.append('/home/sean/windwatchdb/django/windwatcher/')
from django.core.management import setup_environ
import settings 
setup_environ(settings) 


from django.http import HttpResponse
from django.template import Context, loader
from icarus.models import Site, DayOfWeather, logging, WeatherWatchQueue, WeatherTimeSlice, Launch, Landing
#Fancy order preserving function
from uniqify import uniqify
from memoize import memoize

# Get an instance of a logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('icarus/logs.%s' % (__name__))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler) 
logger.setLevel(logging.DEBUG)

TIME_FORMAT = '%Y%m%d%M'

def index(request):
    template = loader.get_template('icarus/index.html')
    site_list = Site.objects.all().order_by('name')
    logger.debug("Getting flyability for %s sites" % site_list)

    #use any day to get some weather list for headers
    weather_list = _get_unique_weather_list(site_list[0])
    flyability_table = _generate_flyability_table(site_list)

    context = Context({
        'conditions_table':flyability_table,
        'weather_list':map(lambda x: x.as_short_human_timestring,weather_list),
        'title':'WingWeather Flyability Chart',
        })
    return HttpResponse(template.render(context))

def site(request, site_id=None):
    template = loader.get_template('icarus/site.html')
    site = Site.objects.get(id=site_id)
    weather_list = _get_unique_weather_list(site)
    flipped_table = []
    max_length = 0
    #NOAA's weird time buckets. I think this is garunteed
    time_to_index = {'01':0, '04':1, '07':2, '10':3, '13':4, '16':5, '19':6, '22': 7}
    times = [{'value':time} for time in ['1:00', '4:00', '7:00', '10:00', '13:00', '16:00', '19:00', '22:00']]
    TABLE_HEIGHT = 8
    flipped_table.append(times)
    for day in weather_list:
        column = [{'value':'No Prediction'} for i in range(TABLE_HEIGHT)]
        for wts in _get_unique_slices_list(day):
            flyability = _get_wts_flyability(site, wts) 
            column[ time_to_index[wts.as_hour()] ] = {'value':flyability}
        flipped_table.append(column)

    flyability_table = zip(*flipped_table)

    context = Context({
        'weather_list':weather_list,
        'conditions_table':flyability_table,
        'site':site,
        'title':'Site Summary',
        })
    return HttpResponse(template.render(context))

def day(request, day=None):
    template = loader.get_template('icarus/day_of_weather.html')
    slices_list = _get_unique_slices_list(day)
    flyability_table = []
    for wts in slices_list:
        flyability_table.append(wts)

    context = Context({
        'wts_list':flyability_table,
        'title':"Weather for " + DayOfWeather.objects.get(id=day).as_long_human_timestring(),
        })
    return HttpResponse(template.render(context))

def site_list(request,site_id=None):
    template = loader.get_template('icarus/site_list.html')
    site_list = Site.objects.all().order_by('name')
    matrix = []
    for site in site_list:
        row = []
        row.append(site.name)
        row.append(site.city)
        row.append(site.state)
        row.append(str(site.lat) + "," + str(site.lon))
        row.append(site.flight_time_window)
        matrix.append(row)

    context = Context({
        'site_list':site_list,
        'site_table':matrix,
        'title':'Site List',
        })
    return HttpResponse(template.render(context))

def about(request):
    template = loader.get_template('icarus/about.html')
    context = Context({
        'title':'About WingWeather',
        })
    return HttpResponse(template.render(context))

#FIXME: need to get cache clearing to work first
#@memoize
def _get_unique_weather_list(site):
    wwq = WeatherWatchQueue.objects.get(relevant_site=site)
    raw_weather_list = DayOfWeather.objects.filter(weather_stream=wwq).order_by('date_it_happens')
    return uniqify(raw_weather_list, lambda x: x.as_machine_timestring())

#@memoize
def _get_unique_slices_list(day):
    weather_slices = WeatherTimeSlice.objects.filter(day_of_occurance=day)
    return uniqify(weather_slices, lambda x: x.id)

def _generate_flyability_table(site_list):
    flyability_table = []
    for site in site_list:
        row = []
        #site name/info
        row.append({'value':site.name,
                    'id':site.id,
                    'link':'site'})

        #flyability ratings
        for day in _get_unique_weather_list(site):
            row.append({'value':site.site_check(day),
                        'id':day.id,
                        'link':'day'})

        flyability_table.append(row)
    return flyability_table

#@memoize
def _get_wts_flyability(site, wts):
    grounds = []
    grounds.append(Launch.objects.filter(site=site))
    grounds.append(Landing.objects.filter(site=site))

    flyability = []
    for ground in grounds:
        time, score = Site.get_wts_flyability(site, ground, wts)
        flyability.append(score)

    return flyability

