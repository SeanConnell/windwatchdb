#Get windwatcher and django on the import path  
import sys
sys.path.append('/home/sean/django/windwatcher') 
from django.core.management import setup_environ 
import settings 
setup_environ(settings) 
from icarus.models import * 
 
"""Pulls weather for a specific site, and puts it into the site's WeatherWatchQueue""" 
def delete_weather(site): 
    #get the watch queue, then delete all weather time slices and days
    wwq = WeatherWatchQueue.objects.filter(relevant_site=site) 
    days = DayOfWeather.objects.filter(weather_stream=wwq)    
    for day in days:
        wtslices = WeatherTimeSlice.objects.filter(day_of_occurance=day)
        for wts in wtslices:
            wts.delete()
        day.delete()
    
