#!/bin/bash
python manage.py reset icarus
python manage.py syncdb --noinput
python import_sites.py
python refresh_weather.py
