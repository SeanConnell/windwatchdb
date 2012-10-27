#!/bin/bash
python manage.py syncdb --noinput
python import_sites.py
python refresh_weather.py
