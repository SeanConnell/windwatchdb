#!/bin/bash
python manage.py syncdb --noinput
python ./icarus/import_sites.py
python ./icarus/refresh_weather.py
