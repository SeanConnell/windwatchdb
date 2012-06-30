from django.db import models
from datetime import datetime as dt
from datetime import timedelta as td
"""TODO: Add self learning statistical observation of accuracy of weather forecast for a particular site by gather actual information on day of vs predicted data and correlate that with both overall accuracy and overall accuracy as a function of forecast time and location"""


"""Holds the two corners of the box defining the site coords for the NWDB lookup as well as name of site and a list of launches and landings"""
class Site(models.Model):
	
	def __init__(self, name="No Name",launches=None,landings=None):
		self.name = name # name of the site	
		self.launches=launches # a list of launch objects
		self.landings=landings # a list of landing objects
	
	def __unicode__(self):
        	return self.name

	name = models.CharField(max_length=200)
	gps_coords_a = models.IntegerField(default=0) # one corner of the rectangle defining this site
	gps_coords_b = models.IntegerField(default=0) # other corner 

"""Holds wind direction in degrees azimuth, velocity (in mph), chance precipitation, temperature, cloudbase, and date of forecast. Also holds actual values for post analysis of data accuracy"""
class Weather(models.Model):	

	def __unicode__(self):
        	return unicode(self.date_it_happens.strftime("%A, %d. %B %Y %I:%M%p"))

	wind_direction_pre = models.IntegerField(default=0)
	wind_direction_obs = models.IntegerField(default=0)
	wind_velocity_pre = models.IntegerField(default=0)
	wind_velocity_obs = models.IntegerField(default=0)
	chance_precipitation = models.IntegerField(default=0)
	temperature_pre = models.IntegerField(default=0)
	temperature_obs = models.IntegerField(default=0)
	cloudbase_pre = models.IntegerField(default=0)
	cloudbase_obs = models.IntegerField(default=0)
	prediction_date = models.DateTimeField()
	date_it_happens = models.DateTimeField()
	

""" A launch and its sea level altitude, acceptable range of wind directions to fly in, and warnings about how to launch"""
class Launch(models.Model):
	name = models.CharField(max_length=200)
	altitude = models.IntegerField(default=0)
	flyable_wind_direction = models.IntegerField(default=0)
	flyable_wind_speed = models.IntegerField(default=0)
	launch_warnings = models.CharField(max_length=50000)

""" A landing and its sea level altitude, and a description of how to do the approach"""	
class Landing(models.Model):
	name = models.CharField(max_length=200)
	altitude = models.IntegerField(default=0)	
	approach_description = models.CharField(max_length=50000)

""" A queue of weather forecasts for a location every time division, uses weather object keys to lookup objects in database as needed. Looks up to the nearest time division by rounding start and end date times """
class WeatherWatchQueue(models.Model):
	def __init__(self,start_date=dt.utcnow(),window=14,end_date=(dt.utcnow() +td(days=14) ) ):
		self.window = window
		self.start_date = start_date #default start date is now
		self.end_date = end_date #default end date is 14 days after now
		
	sample_period = 3 # hours between database updates/list items	
	#start_date = models.DateTimeField()
	#end_date = models.DateTimeField()
	
