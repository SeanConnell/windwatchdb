#!/usr/bin/python

from django.db import models
from datetime import datetime as dt
from datetime import timedelta as td

"""Holds the site coords for the NWDB lookup as well as name of site and a list of launches and landings
A site has only compatible launches and landings, such that any landing can be reached from any launch"""
class Site(models.Model):

    def __unicode__(self):
            return self.name
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=12, decimal_places=6) #lat and lon for the point defining the site
    lon = models.DecimalField(max_digits=12, decimal_places=6)
    last_weather_refresh = models.DateTimeField(null=True)

    #Acts as an enum more or less
    wind_conditions_good = {
        'no lift':False,
        'poor':False,
        'fair':True,
        'good':True,
        'dangerous wind':False
    }

    #Converts various combinations of site possibilities into total site flyability
    #TODO: make this less hackey/proper
    site_conditions = { 'good': {},'fair': {} }
    site_conditions['good']={'good':'Excellent','fair':'Good'}
    site_conditions['fair']={'good':'Good','fair':'Fair'}

    """Checks weather conditions for all landings associated with a site
    Takes a site object
    returns a dict of flyable launches with format [launch_id]:['no lift'|'poor'|'fair'|'good'|'dangerous wind']"""
    #TODO:Fill in stub to pull weather for site and check against landing specifics
    def _landing_check( landing ):
        print "Landing checks for %s on %s landing." % (landing.name,landing.site)
        return {54:'good',63:'good'}

    """Checks weather conditions for all launches associated with a site
    Takes a site object
    returns a dict of flyable launches with format [launch_id]:['no lift'|'poor'|'fair'|'good'|'dangerous wind']"""
    #TODO:Fill in stub to pull weather for site and check against launch specifics
    def _launch_check():
        print "Launch check stub" 
        return {323:'dangerous wind',32:'fair',43:'poor'}

    """Checks if there are at least 1 fair|good launch and 1 'fair'|'good' landing
    Takes a site object
    returns fair if the best case is two are fair, good if one is good, and excellent if both are good"""
    def site_check():
        print "Site check stub" 
        #return list of known words for site conditions, this function is naive about which launch/landing it is, don't care
        #TODO: add in object passing down to private functions
        launchability =  [ flyability for site_id,flyability in _launch_check().iteritems() if wind_conditions_good[flyability] ]
        landability =  [ flyability for site_id,flyability in _landing_check().iteritems() if wind_conditions_good[flyability] ]
        #condense list to best case
        for launch_condition in launchability:
            #if we find good that's it, we're done looking
            if launch_condition == 'good':
                break #else we have fair
        for landing_condition in launchability:
            if landing_condition == 'good':
                break 
        #Lookup overall resultant flyability of site based on launch/landing combos
        return site_conditions[launch_condition][landing_condition] 

"""All weather objects are collected into this queue for easy access"""
class WeatherWatchQueue(models.Model):
    def __unicode__(self):
        return unicode("Days of forecast weather for " + str(self.relevant_site))
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
    warnings = models.CharField(max_length=50000)
    flight_description = models.CharField(max_length=50000)

""" A landing and its sea level altitude, and a description of how to do the approach"""    
class Landing(models.Model):
    def __unicode__(self):
        return unicode(self.name + " landing for " + self.site.name)

    name = models.CharField(max_length=200)
    site = models.ForeignKey(Site)
    altitude = models.IntegerField(default=0)    
    flyable_wind_direction_min = models.IntegerField(default=0)
    flyable_wind_direction_max = models.IntegerField(default=0)
    flyable_wind_speed = models.IntegerField(default=0)
    warnings = models.CharField(max_length=50000)
    flight_description = models.CharField(max_length=50000)
