from django.db import models
from datetime import datetime as dt
from datetime import timedelta as td

"""Holds the site coords for the NWDB lookup as well as name of site and a list of launches and landings"""
class Site(models.Model):
    def __unicode__(self):
            return self.name

    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=12, decimal_places=6) #lat and lon for the point defining the site
    lon = models.DecimalField(max_digits=12, decimal_places=6)

"""Holds wind direction in degrees azimuth, velocity (in mph), chance precipitation, temperature, cloudbase, and date of forecast."""
class Weather(models.Model):    
    def __unicode__(self):
            return unicode(self.date_it_happens.strftime("%A, %d. %B %Y %I:%M%p"))

    wind_direction = models.IntegerField(default=0)
    wind_speed = models.IntegerField(default=0)
    chance_precipitation = models.IntegerField(default=0)
    temperature = models.IntegerField(default=0)
    apparent_temperature = models.IntegerField(default=0)
    cloud_cover_amount = models.IntegerField(default=0)
    prediction_date = models.DateTimeField()
    date_it_happens = models.DateTimeField()

""" A launch and its sea level altitude, acceptable range of wind directions to fly in, and warnings about how to launch"""
class Launch(models.Model):
    name = models.CharField(max_length=200)
    altitude = models.IntegerField(default=0)
    flyable_wind_direction_min = models.IntegerField(default=0)
    flyable_wind_direction_max = models.IntegerField(default=0)
    flyable_wind_speed = models.IntegerField(default=0)
    launch_warnings = models.CharField(max_length=50000)
    launch_description = models.CharField(max_length=50000)

""" A landing and its sea level altitude, and a description of how to do the approach"""    
class Landing(models.Model):
    name = models.CharField(max_length=200)
    altitude = models.IntegerField(default=0)    
    flyable_wind_direction_min = models.IntegerField(default=0)
    flyable_wind_direction_max = models.IntegerField(default=0)
    flyable_wind_speed = models.IntegerField(default=0)
    approach_warnings = models.CharField(max_length=50000)
    approach_description = models.CharField(max_length=50000)

""" A queue of weather forecasts for a location every time division, uses weather object keys to lookup objects in database as needed. Looks up to the nearest time division by rounding start and end date times """
class WeatherWatchQueue(models.Model):
    sample_period = 3 # hours between database updates/list items    
#class WeatherWatchQueue(models.Model):
#    def __init__(self,start_date=dt.utcnow(),window=14,end_date=(dt.utcnow() +td(days=14) ) ):
#        self.window = window
#        self.start_date = start_date #default start date is now
#        self.end_date = end_date #default end date is 14 days after now

#    sample_period = 3 # hours between database updates/list items    
