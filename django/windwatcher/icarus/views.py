# Create your views here.
#for debugging uncomment and run in ipython
import sys
sys.path.append('/home/sean/django/windwatcher') 
from django.core.management import setup_environ 
import settings 
setup_environ(settings) 

from django.http import HttpResponse
from django.template import Context, loader
from icarus.models import *
import datetime, time
def index(request):
    template = loader.get_template('icarus/index.html')
    site_list = Sites.objects.all().order_by('name') 
    weather_list = DayOfWeather.objects.all().order_by('date_it_happens')
    dt_utc = datetime.datetime.utcnow()
    # convert UTC to local time
    dt_local = dt_utc - datetime.timedelta(seconds=time.altzone)
    context = Context({
        'datetime': dt_local.strftime("%A the %d, %B %Y at %r"),
        'site_list':site_list,
        'weather_list':weather_list
        })
    return HttpResponse(template.render(context))

def site(request,site=None):
    template = loader.get_template('icarus/site.html')
    context = Context({
        'site':site,
        })
    return HttpResponse(template.render(context))

def weather_day(request,dofweat=None):
    template = loader.get_template('icarus/day_of_weather.html')
    dofweat = DayOfWeather.objects.get(id=dofweat)
    tslice_list = WeatherTimeSlice.objects.filter(day_of_occurance=dofweat)
    tslice_list.extra(order_by = ['-start_time'])
    context = Context({
        'dofweat':dofweat,
        'tslice_list':tslice_list,
        })
    return HttpResponse(template.render(context))
