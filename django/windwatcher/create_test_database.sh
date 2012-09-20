#!/bin/bash
python manage.py syncdb --noinput
python ./icarus/test_sites.py
python ./icarus/refresh_weather.py
