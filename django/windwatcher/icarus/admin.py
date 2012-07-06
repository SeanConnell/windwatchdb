from icarus.models import Sites, DayOfWeather,WeatherTimeSlice,Launches,Landings,WeatherWatchQueue
from django.contrib import admin

admin.site.register(Sites)
admin.site.register(DayOfWeather)
admin.site.register(WeatherTimeSlice)
admin.site.register(WeatherWatchQueue)
admin.site.register(Launches)
admin.site.register(Landings)
