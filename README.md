windwatchdb
===========

A Django project to predict which days will be good hang gliding days.
Pulls weather data from NOAA's weather service, checks it against a list of known hang gliding sites for flyable conditions, and then alerts interested parties as well as displaying upcoming likely "good" days.

Install notes: Currently there are a bunch of absolute paths the need to be changed in some of the import paths. Also, import sites must be run by hand ONCE, and you need to add a crontab entry for refresh weather, every hour should be sufficient.
