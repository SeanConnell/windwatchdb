#!/usr/bin/python
from django.db import models
import logging
from datetime import datetime
from unflyable import UnflyableError
from join_dict import join_dict, add
from compare_angles import compare_angles
from compare_speed import compare_speed
from empty import empty

# Get an instance of a logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('icarus/logs.%s' % (__name__))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler) 
logger.setLevel(logging.DEBUG)

TIME_FORMAT = '%Y%m%d%M'

"""Holds the site coords for the NWDB lookup as well as name of site and a list of launches and landings
A site has only compatible launches and landings, such that any landing can be reached from any launch"""
class Site(models.Model):

    flyability_metric = {6:"6",5:"5",4:"4",3:"3",2:"2",1:"1",0:"0"}

    def __unicode__(self):
            return self.name


    name = models.CharField(max_length=200)
    nameid = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=12, decimal_places=6) #lat and lon for the point defining the site
    lon = models.DecimalField(max_digits=12, decimal_places=6)
    last_weather_refresh = models.DateTimeField(null=True)
    flight_time_window = "FIXME" #make this a date time range, or if neccesary make a day begin and day end

    #TODO ask John his opinion about these 'fair' 'good' rating systems
    """TODO check sunrise times, they should be in the DayOfWeather. 
    Currently naively assumes 6AM - 5PM as flyable times 
    Might be able to do this with a Django query filter"""

    def site_check(self, day):

        if logger:
            logger.debug("Site check for %s" %(day))

        #this gets us {ground:{time:condition}}
        launch_conditions = self.get_launching_conditions(day)
        landing_conditions = self.get_landing_conditions(day)

        #perform a join to get only common times 
        return self.find_max_flyability(launch_conditions,landing_conditions)

    "Pulls together the launches and landings status and adds values together to get best case flyability"
    def find_max_flyability(self, launches, landings):
        conditions = []
        flyability = []

        for launch in launches:
            for landing in landings:
                conditions.append(join_dict(launches[launch], landings[landing], add))

        for condition in conditions:
            flyability.extend(condition.values())

        if flyability == []:
            raise UnflyableError("Problem joining conditions for flyability calculation. Empty flyability")

        return max(flyability)

    def get_launching_conditions(self, check_day):

        launches_list = Launch.objects.filter(site=self)

        if empty(launches_list):
            raise UnflyableError("No launches for site %s" %self)

        if logger:
            logger.debug("Flyable landings with %s site on %s day" % (self,check_day))
            logger.debug("Launches list is %s" % launches_list)

        return self.get_ground_conditions(launches_list, check_day)

    def get_landing_conditions(self, check_day):

        landing_list = Landing.objects.filter(site=self)

        if empty(landing_list):
            raise UnflyableError("No landings for site %s" %self)

        if logger:
            logger.debug("Landing list is %s" % landing_list)
            logger.debug("Flyable landings with %s site on %s day" % (self,check_day))

        return self.get_ground_conditions(landing_list, check_day)

    "Returns {ground:{time:condition}}"
    def get_ground_conditions(self, ground_list, check_day):
        ground_status = {}
        for ground in ground_list:
            ground_status[ground] = self.get_day_flyability(ground, check_day)
            if logger:
                logger.debug( "Ground check for the %s ground at %s" % (ground.name, ground.site))


        if logger:
            logger.debug("Resultant ground status dict: %s" % (ground_status))

        if empty(ground_status.iteritems()):
            raise UnflyableError("Ground status has no statuses")
        else:
            return ground_status

    "Returns {time:flyability}"
    def get_day_flyability(self, ground, day):
        day_flyability = {}

        weather_slices = WeatherTimeSlice.objects.filter(day_of_occurance=day)

        if empty(weather_slices):
            raise UnflyableError("No weather time slices")

        for wts in weather_slices:
            wts_time,flyability = self.get_wts_flyability(ground, wts)
            day_flyability[wts_time]=flyability

        if logger:
            logger.debug("Flyability for day %s: %s" % (day.id, day_flyability))

        if empty(day_flyability):
            raise UnflyableError("Empty day_flyability")

        return day_flyability

    "Returns a tuple of time,condition"
    def get_wts_flyability(self, ground, wts):
        return (wts.start_time, self.generate_wts_flyability(ground, wts))

    "Returns an int representing flyability"
    def generate_wts_flyability(self, ground, wts):
        #If this wts has flyability, no need to recalculate
        if wts.flyability:
            return int(wts.flyability)

        #FIXME: There is a minimum requirement for both of these, otherwise unflyable
        wts.flyability = Site.flyability_metric[ground.check_wind_speed(wts) + ground.check_wind_dir(wts)]
        wts.save()
        if logger:
            logger.debug("This particular timeslice's flyability: %d" % int(wts.flyability))

        return int(wts.flyability)

"""All weather objects are collected into this queue for easy access"""
class WeatherWatchQueue(models.Model):
    def __unicode__(self):
        return unicode("Days of forecast weather for %s" % str(self.relevant_site))
    relevant_site = models.ForeignKey(Site) #the site the weather is for

"""Holds a bunch of timeslice predictions for that day's weather"""
class DayOfWeather(models.Model):
    def __unicode__(self):
        return unicode(self.date_it_happens.strftime("%A, %d. %B %Y"))

    def as_machine_timestring(self):
        return self.date_it_happens.strftime(TIME_FORMAT)

    def as_long_human_timestring(self):
        return self.date_it_happens.strftime("%A, %d")

    def as_short_human_timestring(self):
        return self.date_it_happens.strftime("%m/%d")

    date_it_happens = models.DateTimeField()
    prediction_date = models.DateTimeField()
    max_temperature = models.IntegerField() #future use
    min_temperature = models.IntegerField() #future use
    weather_stream = models.ForeignKey(WeatherWatchQueue) #holds thew weather for this site
    sunrise = models.DateTimeField(default = datetime.now())
    sunset = models.DateTimeField(default = datetime.now())

    # sort by "the date" in descending order unless
    # overridden in the query with order_by()
    class Meta:
        ordering = ['date_it_happens']

"""A chunk of time for which weather has been predicted. Goes with the DayOfWeather to build out a forecast"""
class WeatherTimeSlice(models.Model):
    def __unicode__(self):
        return unicode("Weather beginning at %s" % str(self.start_time))

    def as_machine_timestring(self):
        return self.start_time.strftime(TIME_FORMAT)

    def as_long_human_timestring(self):
        return self.start_time.strftime("%A, %d")

    def as_short_human_timestring(self):
        return self.start_time.strftime("%m/%d")

    def as_hour(self):
        return self.start_time.strftime("%H")


    #TODO:fix start time having the year and shit in it
    start_time = models.DateTimeField()
    wind_direction = models.IntegerField(default=0)
    wind_speed = models.IntegerField(default=0)
    chance_precipitation = models.IntegerField(default=0)
    temperature = models.IntegerField(default=0)
    apparent_temperature = models.IntegerField(default=0)
    cloud_cover_amount = models.IntegerField(default=0)
    day_of_occurance = models.ForeignKey(DayOfWeather)
    flyability = models.CharField(max_length=50)

    class Meta:
        # sort by "the date" in descending order unless
        # overridden in the query with order_by()
        ordering = ['start_time']

"Ground is whatever various piece of ground (launch, landing, whatever) that is relevant to a hang glider"
class Ground(models.Model):


    tolerances = [0.10,0.20,0.50]
    flyability_of  = {0.10:3,0.20:2,0.50:1}
    speed_tolerance = 0.15 #wind speeds have an additional 15% tolerance
    angle_tolerance = 0.05 #wind angle have an additional 5% tolerance

    class Meta:
        abstract = True
        ordering = ['name']

    #Note: the wind speed and dir should either be relative to the forecasts or use "offset" for the site's effect on weather
    name = models.CharField(max_length=200)
    site = models.ForeignKey(Site)
    altitude = models.IntegerField(default=0)

    #Offsets to try and account for site/local effects
    wind_speed_offset = models.IntegerField(default=0)
    wind_direction_offset = models.IntegerField(default=0)
    flyable_wind_direction = models.IntegerField(default=0)
    flyable_wind_direction_tolerance = models.IntegerField(default=0)
    flyable_wind_speed = models.IntegerField(default=0)
    flyable_wind_speed_tolerance = models.IntegerField(default=0)

    #Possible pitfalls of the launch/landing, things to worry about
    warnings = models.CharField(max_length=50000)
    #How to correctly launch/land here
    flight_description = models.CharField(max_length=50000)

    "Get tolerance rating for wind,angle,etc"
    def check_tolerance(self, given, desired, condition_tolerance, acceptable_tolerance):
        for percent_tolerance in Ground.tolerances:
            tolerance = round(percent_tolerance*desired) + condition_tolerance
            if acceptable_tolerance(given, desired, tolerance):
                return Ground.flyability_of[percent_tolerance]
        return 0 #Default case is unflyable aka 0

    def check_wind_speed(self, wts):
        """Duck typing at work, read it like:
        check the windspeed for flyably wind
        speeds with this tolerance using compare speed"""
        return self.check_tolerance(
                wts.wind_speed, 
                self.flyable_wind_speed, 
                self.speed_tolerance, 
                compare_speed)
 
    def check_wind_dir(self, wts):
        #Same as above, except for wind direction (angle)
        return self.check_tolerance(
                wts.wind_direction, 
                self.flyable_wind_speed, 
                self.angle_tolerance, 
                compare_angles)

"A launch zone"
class Launch(Ground):

    type = "launch"

    def __unicode__(self):
        return unicode("%s launch for %s" % (self.name, self.site.name))

    class Meta(Ground.Meta):
        db_table = 'launch_info'

"A landing zone"
class Landing(Ground):

    type = "landing"

    def __unicode__(self):
        return unicode("%s landing for %s" % (self.name, self.site.name))

    class Meta(Ground.Meta):
        db_table = 'launding_info'
