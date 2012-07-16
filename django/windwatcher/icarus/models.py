from django.db import models
from datetime import datetime as dt
from datetime import timedelta as td

"""Holds the site coords for the NWDB lookup as well as name of site and a list of launches and landings"""
class Site(models.Model):
    def __unicode__(self):
            return self.name
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=12, decimal_places=6) #lat and lon for the point defining the site
    lon = models.DecimalField(max_digits=12, decimal_places=6)
    last_weather_refresh = models.DateTimeField(null=True)

"""All weather objects are collected into this queue for easy access"""
class WeatherWatchQueue(models.Model):
    #probably don't actually need these fields, will add back in if I want them
    #start_date = models.DateTimeField() 
    #end_date = models.DateTimeField() 
    #number_of_days = models.IntegerField() #current number of days there exists data for
    relevant_site = models.ForeignKey(Site) #which site the weather is for

"""Holds a bunch of timeslice predictions for that day's weather"""
class DayOfWeather(models.Model):
    def __unicode__(self):
        return unicode(self.date_it_happens.strftime("%A, %d. %B %Y"))

    date_it_happens = models.DateTimeField()
    prediction_date = models.DateTimeField()
    max_temperature = models.IntegerField() #future use
    min_temperature = models.IntegerField() #future use
    weather_stream = models.ForeignKey(WeatherWatchQueue) #holds thew weather for this site

    class Meta:
        # sort by "the date" in descending order unless
        # overridden in the query with order_by()
        ordering = ['date_it_happens']

"""A chunk of time for which weather has been predicted. Goes with the DayOfWeather to build out a forecast"""
class WeatherTimeSlice(models.Model):
    def __unicode__(self):
        return unicode("Weather beginning at " + str(self.start_time))

    start_time = models.DateTimeField()
    wind_direction = models.IntegerField(default=0)
    wind_speed = models.IntegerField(default=0)
    chance_precipitation = models.IntegerField(default=0)
    temperature = models.IntegerField(default=0)
    apparent_temperature = models.IntegerField(default=0)
    cloud_cover_amount = models.IntegerField(default=0)
    day_of_occurance = models.ForeignKey(DayOfWeather)

    class Meta:
        # sort by "the date" in descending order unless
        # overridden in the query with order_by()
        ordering = ['start_time']

""" A launch and its sea level altitude, acceptable range of wind directions to fly in, and warnings about how to launch"""
class Launch(models.Model):
    def __unicode__(self):
        return unicode(self.name + " launch for " + self.site.name)

    name = models.CharField(max_length=200)
    site = models.ForeignKey(Site)
    altitude = models.IntegerField(default=0)
    flyable_wind_direction_min = models.IntegerField(default=0)
    flyable_wind_direction_max = models.IntegerField(default=0)
    flyable_wind_speed = models.IntegerField(default=0)
    launch_warnings = models.CharField(max_length=50000)
    launch_description = models.CharField(max_length=50000)

""" A landing and its sea level altitude, and a description of how to do the approach"""    
class Landing(models.Model):
    name = models.CharField(max_length=200)
    site = models.ForeignKey(Site)
    altitude = models.IntegerField(default=0)    
    flyable_wind_direction_min = models.IntegerField(default=0)
    flyable_wind_direction_max = models.IntegerField(default=0)
    flyable_wind_speed = models.IntegerField(default=0)
    approach_warnings = models.CharField(max_length=50000)
    approach_description = models.CharField(max_length=50000)

#class DatabaseUpdating(models.Model):
# do something like this, though this doesn't seem proper, to not let people see a blown up database when stuff is updating    
