#!/bin/bash
python manage.py syncdb --noinput
python test_sites.py
python refresh_weather.py
