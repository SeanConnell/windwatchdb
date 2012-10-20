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

sollie = Site(name="Sollie Smith",lat=45.476624,lon=-123.787594,city="Tillamook",state="Oregon")
kiwanda = Site(name="Cape Kiwanda",lat="45.224007",lon="-123.97316",city="Pacific City",state="Oregon")
petersons_top = Site(name="Peterson's Butte",lat=44.441134,lon=-123.013916,city="Corvallis",state="Oregon")
petersons_bot = Site(name="Peterson's Butte",lat=44.441134,lon=-123.013916,city="Corvallis",state="Oregon")
dog = Site(name="Dog Mountain",lat=46.471325,lon=-122.168312,city="Morton",state="Washington")
cape_lookout = Site(name="Cape Lookout",lat=45.342494,lon=-123.978653,city="Tillamook",state="Oregon")
oceanside = Site(name="Oceanside",lat=45.462057,lon=-123.969727,city="Oceanside",state="Oregon")

site_list = [sollie,kiwanda,petersons_top,petersons_bot,dog,cape_lookout,oceanside]

print "Importing site list"
for site in site_list:
    site.save()
    print "Saving",site

sollie_w = Launch(name="West",site=sollie,flyable_wind_speed_min=7,flyable_wind_speed_max=15,flyable_wind_direction_min=240,flyable_wind_direction_max=330)
sollie_n = Launch(name="North",site=sollie,flyable_wind_speed_min=8,flyable_wind_speed_max=16,flyable_wind_direction_min=300,flyable_wind_direction_max=330)
kiwanda_nnw = Launch(name="NNW",site=kiwanda)
petersons_lower = Launch(name="Lower Launch",site=petersons_top)
petersons_upper = Launch(name="Upper Launch",site=petersons_bot)
dog_north = Launch(name="North",site=dog)
dog_west = Launch(name="West",site=dog)
cape_lookout_nw= Launch(name="NW",site=cape_lookout)
oceanside_wnw = Launch(name="WNW",site=oceanside)

launch_list = [sollie_n,sollie_w,kiwanda_nnw,petersons_lower,petersons_upper,dog_north,dog_west,cape_lookout_nw,oceanside_wnw]

for launch in launch_list:
    launch.save()
    print "Saving",launch

sollie_nw_small_field = Landing(name="Small, Cowless Field",site=sollie)
sollie_sw_small_field = Landing(name="Large, Cow Field",site=sollie)
sollie_se_small_field = Landing(name="Smaller, Cow Field",site=sollie)
sollie_ne_small_field = Landing(name="Larger, Cowless Field",site=sollie)
kiwanda_beach = Landing(name="Lower Beach",site=kiwanda)
kiwanda_top = Landing(name="Dune Top",site=kiwanda)
petersons_west_long= Landing(name="Further Field for top launch",site=petersons_bot)
petersons_west_short = Landing(name="Shorter Field for top launch",site=petersons_bot)
petersons_south_short = Landing(name="Shorter Field before power lines",site=petersons_top)
petersons_south_long = Landing(name="Longer Field after power lines",site=petersons_top)
dog_beach = Landing(name="Landing Field When Water is Low",site=dog)
dog_swamp = Landing(name="Landing Field When Water is High",site=dog)
cape_lookout_beach = Landing(name="Beach",site=cape_lookout)
oceanside_beach = Landing(name="Beach",site=oceanside)

landing_list = [sollie_nw_small_field,sollie_sw_small_field,sollie_se_small_field,sollie_ne_small_field,kiwanda_beach,\
kiwanda_top,petersons_west_long,petersons_west_short,petersons_south_long,petersons_south_short,dog_beach,dog_swamp,\
cape_lookout_beach,oceanside_beach]

for landing in landing_list:
    landing.save()
    print "Saving",landing

#Create WWQs here after Sites have IDs
wwq1 = WeatherWatchQueue(relevant_site=sollie)
wwq2 = WeatherWatchQueue(relevant_site=kiwanda)
wwq3 = WeatherWatchQueue(relevant_site=petersons_bot)
wwq4 = WeatherWatchQueue(relevant_site=petersons_top)
wwq5 = WeatherWatchQueue(relevant_site=dog)
wwq6 = WeatherWatchQueue(relevant_site=cape_lookout)
wwq7 = WeatherWatchQueue(relevant_site=oceanside)
wwq_list = [wwq1,wwq2,wwq3,wwq4,wwq5,wwq6,wwq7]

for wwq in wwq_list:
    wwq.save()
    print "Saving",wwq


