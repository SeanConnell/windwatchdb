from django.test import TestCase
from icarus.models import Site,Launch,Landing,WeatherTimeSlice,DayOfWeather,Ground

class LaunchTest(TestCase):

    fixtures = ['icarus_models_test_data.json']

    def setUp(self):

        """test launch has these values:
            fly_wspd: 12
            wind_tol:  3
            fly_wdir:180
            wdir_tol: 45
        """
        self.test_launch = Launch.objects.get(pk=1)
        self.test_wts = WeatherTimeSlice.objects.get(pk=34)

    def test_check_tolerance(self):
        pass

    def test_check_wind_speed_3(self):
        self.test_wts.wind_speed = 12
        test_flyability = self.test_launch.check_wind_speed(self.test_wts)
        self.assertEqual(test_flyability, 3)

    def test_check_wind_speed_2(self):
        self.test_wts.wind_speed = 8 
        test_flyability = self.test_launch.check_wind_speed(self.test_wts)
        self.assertEqual(test_flyability, 2)

    def test_check_wind_speed_1(self):
        self.test_wts.wind_speed = 5 
        test_flyability = self.test_launch.check_wind_speed(self.test_wts)
        self.assertEqual(test_flyability, 1)

    def test_check_wind_speed_0(self):
        self.test_wts.wind_speed = 2 
        test_flyability = self.test_launch.check_wind_speed(self.test_wts)
        self.assertEqual(test_flyability, 0)

    def test_check_wind_direction_3(self):
        self.test_wts.wind_direction = 180
        test_flyability = self.test_launch.check_wind_dir(self.test_wts)
        self.assertEqual(test_flyability, 3)

    def test_check_wind_direction_2(self):
        self.test_wts.wind_direction = 130
        test_flyability = self.test_launch.check_wind_dir(self.test_wts)
        self.assertEqual(test_flyability, 2)

    def test_check_wind_direction_1(self):
        self.test_wts.wind_direction = 70
        test_flyability = self.test_launch.check_wind_dir(self.test_wts)
        self.assertEqual(test_flyability, 1)

    def test_check_wind_direction_0(self):
        self.test_wts.wind_direction = 20 
        test_flyability = self.test_launch.check_wind_dir(self.test_wts)
        self.assertEqual(test_flyability, 0)

class SiteTest(TestCase):

    fixtures = ['icarus_models_test_data.json']

    def setUp(self):
        self.site1 = Site.objects.get(pk=1)
        self.site2 = Site.objects.get(pk=2)

    "Found a bug where an empty flyability can happen, and the max function hates that"
    def test_empty_flyability_in_find_max_flyability(self):
        pass

    "TODO: Test all the function models for empty input args or things that will generate empty output args"
