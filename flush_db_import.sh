#!/bin/bash
if $1 -eq "admin"
then
python manage.py reset icarus
python manage.py syncdb 
python import_sites.py
python refresh_weather.py
else
python manage.py reset icarus
python manage.py syncdb --noinput
python import_sites.py
python refresh_weather.py
fi

