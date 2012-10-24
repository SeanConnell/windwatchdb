from icarus.models import Site,DayOfWeather,WeatherTimeSlice,Launch,Landing,WeatherWatchQueue
from django.contrib import admin

admin.site.register(Site)
admin.site.register(DayOfWeather)
admin.site.register(WeatherTimeSlice)
admin.site.register(WeatherWatchQueue)
admin.site.register(Launch)
admin.site.register(Landing)
