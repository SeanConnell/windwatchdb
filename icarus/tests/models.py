"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from icarus.models import Site,Launch,Landing,WeatherTimeSlice,DayOfWeather

class LaunchTest(TestCase):
    fixtures = ['icarus_models_test_data.json']

    """
    test_site = Site.objects.create(
            name="Test Site One",
            lat=45.476624,
            lon=-123.787594,
            city="Testcity",
            state="TestState")

    test_launch = Launch.objects.create(
            name="Test Launch",
            site=test_site,
            flyable_wind_direction=180,
            flyable_wind_direction_tolerance=45,
            flyable_wind_speed=12,
            flyable_wind_speed_tolerance=3)

    test_wts = WeatherTimeSlice.objects.create(
            start_time=datetime.now(),
            day_of_occurance=None,
            wind_direction=175,
            wind_speed=9)
    """

    def test_check_tolerance(self):
        pass

    def test_check_wind_speed(self):
        pass

    def test_check_wind_direction(self):
        pass

class SiteTest(TestCase):

    "Found a bug where an empty flyability can happen, and the max function hates that"
    def test_empty_flyability_in_find_max_flyability():
        pass

    "TODO: Test all the function models for empty input args or things that will generate empty output args"

