#!/usr/bin/python
import sys
from datetime import date, timedelta
from datetime import datetime 
import re


#Get windwatcher and django on the import path
#Fix this later
import getpass
user = getpass.getuser()
spath = "/home/" +  user + "/windwatchdb/django/windwatcher"
sys.path.append(spath)
from django.core.management import setup_environ
import settings
setup_environ(settings)
from icarus.models import * 

#Acts as a constant time lookup for if a condition is good or not
wind_conditions_good = {
    'no lift':False,
    'poor':False,
    'fair':True,
    'good':True,
    'dangerous wind':False,
    'too cross':False
}

#Converts various combinations of site possibilities into total site flyability
#TODO: make this less hackey and more proper
site_conditions = { 'good': {},'fair': {} }
site_conditions['good']={'good':'Excellent','fair':'Good'}
site_conditions['fair']={'good':'Good','fair':'Fair'}

flight_time_window = "FIXME" #make this a date time range, or if neccesary make a day begin and day end

"""Actually does the boilerplate of checking weather conditions using duck typing
Takes a launch/landing and a wts 
returns 'no lift'|'poor'|'fair'|'good'|'dangerous wind'
where no lift is <25% min speed, poor is 25<min<100. If delta = (max-min)./4, then good is (max+min).2/ -+delta
everything else is fair. All wind directions must be within the middle 2/3 of the wind angle to get a good rating 
if not, they get fair. If no in the range at all, get not flyable"""
#TODO ask John his opinion about these 'fair' 'good' rating systems
def _timeslice_flight_check( ground, wts ):
    #If this wts has flyability, no need to recalculate
    if wts.flyability:
        return wts.flyability
    #Otherwise we're at a new wts, time to get mins and maxes and calculate deltas
    print "flyable wind speed: %d - %d" % (ground.flyable_wind_speed_min ,ground.flyable_wind_speed_max)
    print "flyable wind andle: %d - %d" % (ground.flyable_wind_direction_min ,ground.flyable_wind_direction_max)
    #Flyable values for this launch/landing
    amax,amin = (ground.flyable_wind_direction_max + ground.wind_direction_offset, ground.flyable_wind_direction_min + ground.wind_direction_offset)
    smax,smin = (ground.flyable_wind_speed_max + ground.wind_speed_offset, ground.flyable_wind_speed_min + ground.wind_speed_offset)
    aavg,savg = ((amax+amin)./2,(smax+smin)./2)
    #deltas for calculating good conditions
    a_d,s_d = ((amax + amin)./3, (smax + smin)./4)
    #Actual weather for this weather time slice (wts)
    wspe,wdir = (wts.wind_direction,wts.wind_speed)
    #check various conditions
    #get the easy ones out of the way first
    wts.flyability = 'no lift' if wspe < .25*smin 
    wts.flyability = 'poor' if wspe < smin 
    wts.flyability = 'dangerous wind' if wspe > smax 
    wts.flyability = 'too cross' if amax < wdir < amix 
    if savg - a_d < wspe < savg + a_d: #if the speed is in the sweet spot
        wts.flyability = 'good' if aavg - a_d < wdir < aavg + a_d else wts.flyability = 'fair' #good if dir is also in sweet spot, otherwise fair
    wts.flyability ='fair' #if it isn't no lift, poor, dangerous wind, or good, it must be fair
    wts.save()
    return wts.flyability

"""returns a list of dicts of wts start times {start_time:condition} eg {some_dt_object:'fair'}"""
#TODO check sunrise times. Currently naively assumes 6AM - 5PM as flyable times
def _day_flight_check( ground, wts_day ):
    conditions = []
    for wts in WeatherTimeSlice.objects.filter(day_of_occurance=wts_day):
        #Add all the timeslice conditions to the list
        conditions.append({wts.start_time:_timeslice_flight_check(ground, wts)})
    daytime_conditions = [ condition for start_time,condition in conditions if "6AM FIXME" < start_time < "5PM FIXME" ]
    return daytime_conditions

"""Checks weather conditions for all landings associated with a site
Takes a site object
returns a dict of flyable launches and wts landing ids and dicts of wts statuses
format: {landing.id:[{start_time:condition},more of those 1 entry dicts, etc]}"""
def _landing_check( site,check_day):
    landing_status_dict = {}
    landing_list = Launch.objects.filter(site=site)
    for landing in landing_list:
        print "Landing check for the %s landing at %s" % (landing.name,landing.site) 
        landing_status_dict[landing.id] = _day_flight_check( landing, check_day) 
    return landing_status_dict

"""Checks weather conditions for all launches associated with a site
Takes a site object
returns a dict of flyable launches with format [launch_id]:['no lift'|'poor'|'fair'|'good'|'dangerous wind']"""
def _launch_check( site ):
    print "Unimplemented function launch_check"

"""Checks if there are at least 1 fair|good launch and 1 'fair'|'good' landing
Takes a site object and a day of weather to check against
returns fair if the best case is two are fair, good if one is good, and excellent if both are good"""
def site_check( site , day , timelist=False):
    print "Site check stub" 
    #return list of known words for site conditions, this function is naive about which launch/landing it is, don't care
    landings_conditions = [ condition_list for launch_id,condition_list in _landing_check(site,day).iteritems()]
    landability =  [ flyability for start_time,flyability in landings_conditions if wind_conditions_good[flyability] ]
    #condense list to best case
    for launch_condition in launchability:
        #if we find a good that's it, we're done looking because we report the best condition of the day
        if launch_condition == 'good':
            break #else we have fair
    for landing_condition in launchability:
        if landing_condition == 'good':
            break 
    #Lookup overall resultant flyability of site based on launch/landing combos
    print site_conditions[launch_condition][landing_condition] 


if __name__ == "__main__":
    from _update_weather import update_weather
    #Create a test site, save it, get weather for it, and run these functions on it
    test_site = Site(name="Test Site",lat="45.224007",lon="-123.97316",city="Pacific City",state="Oregon")
    test_site.save()
    test_launch = Launch(name="Test Launch West",site=test_site)
    test_launch.save()
    test_landing = Landing(name="Test Landing West",site=test_site)
    test_landing.save()
    test_wwq = WeatherWatchQueue(relevant_site=test_site)
    test_wwq.save()
    #update the wwq 
    update_weather(test_site)
    #we now have a legit site with a launch, landing, and weather queue. Test away!
    site_check(test_site)
    #cleanup the DB
    test_site.delete()
    test_launch.delete()
    test_landing.delete()
    test_wwq.delete()
