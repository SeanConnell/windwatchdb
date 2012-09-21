#!/usr/bin/python
from django.db import models
from datetime import datetime as dt
from datetime import time
from datetime import timedelta as td
#from settings import TIME_FORMAT
# import the logging library
import logging

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

    def __unicode__(self):
            return self.name
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=12, decimal_places=6) #lat and lon for the point defining the site
    lon = models.DecimalField(max_digits=12, decimal_places=6)
    last_weather_refresh = models.DateTimeField(null=True)
    flight_time_window = "FIXME" #make this a date time range, or if neccesary make a day begin and day end

    """Actually does the boilerplate of checking weather conditions using duck typing
    Takes a launch/landing and a wts 
    returns 'no lift'|'poor'|'fair'|'good'|'dangerous wind'
    where no lift is <25% min speed, poor is 25<min<100. If delta = (max-min)./4, then good is (max+min).2/ -+delta
    everything else is fair. All wind directions must be within the middle 2/3 of the wind angle to get a good rating 
    if not, they get fair. If no in the range at all, get not flyable"""
    #TODO ask John his opinion about these 'fair' 'good' rating systems

    #Acts as a constant time lookup for if a condition is good or not
    wind_conditions_good = {
        'no lift':False,
        'poor':False,
        'fair':True,
        'good':True,
        'dangerous wind':False,
        'too cross':False
    }

    def empty(self, seq):
        try:
            return all(map(self.empty, seq))
        except TypeError:
            return False

    def _timeslice_flight_check(self, ground, wts):
        #TODO Move all of this wind speed logic into the ground object
        #If this wts has flyability, no need to recalculate
        if wts.flyability:
            return wts.flyability
        #Otherwise we're at a new wts, time to get mins and maxes and calculate deltas
        logger.debug( "checking against this speed:   %d" % (wts.wind_speed))
        logger.debug( "flyable wind angle: %d - %d" % (ground.flyable_wind_direction_min ,ground.flyable_wind_direction_max))
        logger.debug( "checking against this dir  :   %d" % (wts.wind_direction))
        
        #Flyable values for this launch/landing
        amax,amin = (ground.flyable_wind_direction_max + ground.wind_direction_offset, ground.flyable_wind_direction_min + ground.wind_direction_offset)
        smax,smin = (ground.flyable_wind_speed_max + ground.wind_speed_offset, ground.flyable_wind_speed_min + ground.wind_speed_offset)
        aavg,savg = ((amax+amin)/2.0,(smax+smin)/2.0)
        #deltas for calculating good conditions
        a_d,s_d = ((amax + amin)/3.0, (smax + smin)/4.0)
        #Actual weather for this weather time slice (wts)
        wdir,wspe = (wts.wind_direction,wts.wind_speed)
        #check various conditions
        #get the easy ones out of the way first
        #import pdb; pdb.set_trace()
        if wspe < .25*smin:
            wts.flyability = 'no lift' 
        elif wspe < smin:
            wts.flyability = 'poor' 
        elif wspe > smax: 
            wts.flyability = 'dangerous wind' 
        elif amax < wdir < amin:
            wts.flyability = 'too cross' 
        elif savg - a_d < wspe < savg + a_d: #if the speed is in the sweet spot
            if aavg - a_d < wdir < aavg + a_d: #good if dir is also in sweet spot, otherwise fair
                wts.flyability = 'good' 
            else:
                wts.flyability = 'fair' 
        else:
            wts.flyability ='fair' #if it isn't no lift, poor, dangerous wind, or good, it must be fair
        wts.save()
        logger.debug("wts object: %s, flyability: %s" % (wts,wts.flyability))
        return wts.flyability

    """returns a list of dicts of wts start times {start_time:condition} eg {some_dt_object:'fair'}"""
    #TODO check sunrise times. Currently naively assumes 6AM - 5PM as flyable times
    def _day_flight_check(self, ground, wts_day):
        conditions_list = []
        for wts in WeatherTimeSlice.objects.filter(day_of_occurance=wts_day):
            #Add all the timeslice conditions to the list
            conditions_list.append({wts.start_time:self._timeslice_flight_check(ground, wts)})
        logger.debug("Resultant wts-es that were in flyable days with their flyability: %s" % (conditions_list))
        daytime_conditions = [[conditions for start_time,condition in conditions.iteritems() if time(hour=6) < start_time.time() < time(hour=17)] for conditions in conditions_list]
        logger.debug("wts-es that were in daytime: %s" % daytime_conditions)
        return daytime_conditions

    """Checks weather conditions for all landings associated with a site
    Takes a site object
    returns a dict of flyable launches and wts landing ids and dicts of wts statuses
    format: {landing.id:[{start_time:condition},more of those 1 entry dicts, etc]}"""
    def _landing_check(self, site, check_day):
        landing_status_dict = {}
        landing_list = Landing.objects.filter(site=site)
        for landing in landing_list:
            logger.debug( "Landing check for the %s landing at %s" % (landing.name, landing.site))
            landing_status_dict[landing.id] = self._day_flight_check(landing, check_day)
        logger.debug("Resultant landing status dict: %s" % (landing_status_dict))
        return landing_status_dict

    """Checks weather conditions for all launches associated with a site
    Takes a site object
    returns a dict of flyable launches with format [launch_id]:['no lift'|'poor'|'fair'|'good'|'dangerous wind']"""
    def _launching_check(self, site, check_day):
        launch_status_dict = {}
        launch_list = Launch.objects.filter(site=site)
        for launch in launch_list:
            logger.debug( "Launching check for the %s landing at %s" % (launch.name,launch.site) )
            launch_status_dict[launch.id] = self._day_flight_check( launch, check_day) 
        logger.debug("Resultant launching dict: %s" % (launch_status_dict))
        return launch_status_dict

    """Deals with merging conditions, should just make this a fuckin' int
    Excellent is two goods
    good is one good one fair
    fair is two fairs
    nothing means unflyable"""
    def _add_timeslice_condition(self, weather, time, condition):
        #FIXME get settings imports working to use settings.TIME_FORMAT
        time = time.strftime(TIME_FORMAT)
        logger.debug("time: %s, condition %s" %(time,condition))
        logger.debug("Weather: %s" % weather)
        acceptable_conditions = ['good','fair']
        if condition not in acceptable_conditions: # keep this restricted to known inputs here... 
            logger.debug("Weather condition not acceptable, got: %s" % condition)
            return # we won't use anything but good conditions 
        logger.debug("Weather condition acceptable, got: %s" % condition)
        if time in weather.keys():
            if weather[time] == 'Excellent':
                logger.debug("Set to Excellent")
                return
            elif weather[time] == 'Good': 
                if condition == 'good':
                    weather[time] = 'Excellent'
                    logger.debug("Set to Excellent")
            elif weather[time] == 'Fair':
                if condition == 'good':
                    weather[time] = 'Good'
                    logger.debug("Set to Good")
        else:
            weather[time] = "Fair"
            logger.debug("Set to Fair")
        logger.debug("Edited weather: %s" % weather)

    """Checks if there are at least 1 fair|good launch and 1 'fair'|'good' landing
    Takes a site object and a day of weather to check against
    returns fair if the best case is two are fair, good if one is good, and excellent if both are good"""
    def site_check(self, site, day):
        flyability_dict = {}
        #day is passed as id
        #day = DayOfWeather.objects.get(id=day_id)
        logger.debug("Site check for %s" %(day))
        landing_list = Landing.objects.filter(site=site)
        unflyable = 'Unflyable'
        possible_conditions = ['Excellent', 'Good', 'Fair', 'Poor']
        #return list of known words for site conditions, this function is naive about which launch/landing it is, don't care. We are looking for total flyability
        landings_conditions = [ condition_list for launch_id,condition_list in self._landing_check(site,day).iteritems()]
        logger.debug( "landing conditions: %s" % (landings_conditions))
        if self.empty(landings_conditions):
            logger.debug("Empty landing zero")
            return unflyable
        #landability =  [ flyability for start_time,flyability in landings_conditions if wind_conditions_good[flyability] ]
        #TODO: Fix this list comprehension BS with lists everywhere
        for timeslice_condition in landings_conditions[0]:
            if not self.empty(timeslice_condition):
                for start_time,flyability in timeslice_condition[0].iteritems():
                    logger.debug("st time: %s, flyability %s" % (start_time,flyability))
                    logger.debug("Flyability dict: %s" % (flyability_dict))
                    self._add_timeslice_condition(flyability_dict,start_time,flyability)
                    logger.debug("Flyability dict: %s" % (flyability_dict))
        launching_conditions = [ condition_list for launch_id,condition_list in self._launching_check(site,day).iteritems()]
        if self.empty(launching_conditions):
            logger.debug("empty launch first")
            return unflyable
        for timeslice_condition in launching_conditions[0]:
            logger.debug("Timeslice: %s" %(timeslice_condition))
            if not self.empty(timeslice_condition):
                for start_time,flyability in timeslice_condition[0].iteritems():
                    self._add_timeslice_condition(flyability_dict,start_time,flyability)
        logger.debug("Checking emptiness of flyabiilty dict: %s" %(flyability_dict))
        #if self.empty(flyability_dict):
        if flyability_dict.keys() == [] or flyability_dict.values() == []:
            logger.debug("empty flyability second")
            return unflyable
        #logger.debug( flyability_dict)
        #Conditions are ordered from best to worst to always return best case
        logger.debug("Iterating over flyability dict: %s" % (flyability_dict))
        for condition in possible_conditions:
            #logger.debug( condition,flyability_dict.values())
            if condition in flyability_dict.values():
                logger.debug("Returning this: %s" % (condition))
                return condition
        #return flyability_dict

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

    def as_machine_timestring(self):
        return self.date_it_happens.strftime(TIME_FORMAT)

    def as_human_timestring(self):
        return self.date_it_happens.strftime("%A, %d")

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
        return unicode("Weather beginning at %s" % str(self.start_time))
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

    class Meta:
        abstract = True
        ordering = ['name']

    "Returns a boolean if a wind angle is in the correct range for flight"
    def angle_in_range(self,angle):
        print "Implement me!"
        return True
    "Returns a boolean if a wind speed is in the correct range for flight"
    def speed_in_range(self,speed):
        print "Implement me!"
        return True

    #Note: the wind speed and dir should either be relative to the forecasts or use "offset" for the site's effect on weather
    name = models.CharField(max_length=200)
    site = models.ForeignKey(Site)
    altitude = models.IntegerField(default=0)
    #Offsets to try and account for site/local effects
    wind_speed_offset = models.IntegerField(default=0)
    wind_direction_offset = models.IntegerField(default=0)
    flyable_wind_direction_min = models.IntegerField(default=0)
    flyable_wind_direction_max = models.IntegerField(default=0)
    flyable_wind_speed_min = models.IntegerField(default=0)
    flyable_wind_speed_max = models.IntegerField(default=0)
    #Possible pitfalls of the launch, things to worry about
    warnings = models.CharField(max_length=50000)
    #How to correctly launch here
    flight_description = models.CharField(max_length=50000)

"A launch zone"
class Launch(Ground):
    #TODO: The min/max angle thing is broken as it has problems going around 0. Need to rewrite it

    def __unicode__(self):
        return unicode(self.name + " launch for " + self.site.name)

    class Meta(Ground.Meta):
        db_table = 'launch_info'


"A landing zone"
class Landing(Ground):

    def __unicode__(self):
        return unicode(self.name + " landing for " + self.site.name)

    class Meta(Ground.Meta):
        db_table = 'launding_info'
