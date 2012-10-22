"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from icarus.models import Ground,Launch,Landing,WeatherTimeSlice
from compare_angles import compare_angles
from compare_speed import compare_speed
from join_dict import join_dict, add
from datetime import datetime

class GroundTest(TestCase):

    """
    test_launch = Ground.objects.create(
            name="Test Launch",
            site=None,
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

class JoinDictTest(TestCase):

    def test_int_keyed_int_valued_dicts(self):
        a = {'a':1,'b':2,'c':3}
        b = {'a':6,'b':5,'c':4}
        expected_result = {'a':7,'b':7,'c':7} 

        self.assertEqual(join_dict(a, b, add), expected_result)

    def test_string_keyed_int_valued_dicts(self):
        a = {1:1,2:2,3:3,4:4,5:5,6:6}
        b = {6:6,5:5,4:4,3:3,2:2,1:1}
        expected_result = {1:2,2:4,3:6,4:8,5:10,6:12}

        self.assertEqual(join_dict(a, b, add), expected_result)

    #Because you never know when 1 + 1 might not be 2
    def test_add_func(self):
        self.assertEqual(add(1,1),2)

class CompareSpeedTest(TestCase):

    def test_in_tol_given_above(self):
        self.assertTrue(compare_speed(10,7,5))

    def test_in_tol_target_above(self):
        self.assertTrue(compare_speed(7,10,5))

    #Negative speeds not allowed; should raise exception
    def test_in_tol_negative_given(self):
        try:
            compare_speed(-10, 7, 5)
        except ValueError:
            pass
        except Exception, e:
            self.fail("Unexpected exception raised", e)
        else:
            self.fail("Expected exception not raised")

    def test_in_tol_negative_target(self):
        try:
            compare_speed(10, -7, 5)
        except ValueError:
            pass
        except Exception, e:
            self.fail("Unexpected exception raised", e)
        else:
            pass

    #Allow negative tolerances, we'll just abs() it. 
    #It's valid to think of a tolerance as negative
    def test_neg_tol_in_range(self):
        self.assertTrue(compare_speed(10,7,-5))

    def test_neg_tol_outside_range(self):
        self.assertFalse(compare_speed(10,3,-5))

class CompareAngleTest(TestCase):

    #test cases for non wrapping angle tolerances
    def test_in_tol_given_above(self):
        self.assertTrue(compare_angles(180, 150, 45))

    def test_in_tol_target_above(self):
        self.assertTrue(compare_angles(150, 180, 45))

    def test_in_tol_angles_same(self):
        self.assertTrue(compare_angles(180, 180, 45))

    def test_in_tol_distance_equal_to_tol_given_above(self):
        self.assertTrue(compare_angles(180, 150, 30))

    def test_in_tol_distance_equal_to_tol_target_above(self):
        self.assertTrue(compare_angles(150, 180, 30))

    #Test angles wrapping around 0/360
    def test_in_tol_wrapped_around_positive(self):
        self.assertTrue(compare_angles(330, 60, 120))

    def test_in_tol_wrapped_around_negative(self):
        self.assertTrue(compare_angles(60, 330, 120))

    def test_all_angle_tol_by_wrap(self):
        self.assertTrue(compare_angles(1,359,180))

    def test_all_angle_tol_no_wrap(self):
        self.assertTrue(compare_angles(1,359,360))

    def test_all_360_0_wrap_negative(self):
        self.assertTrue(compare_angles(0,360,15))

    def test_all_360_0_wrap_positive(self):
        self.assertTrue(compare_angles(0,360,15))

    def test_outside_tol_given_above(self):
        self.assertFalse(compare_angles(180, 90, 45))

    def test_outside_tol_target_above(self):
        self.assertFalse(compare_angles(90, 180, 45))

    def test_outside_tol_by_one_given_above(self):
        self.assertFalse(compare_angles(90, 180, 89))

    def test_outside_tol_by_one_target_above(self):
        self.assertFalse(compare_angles(180, 90, 89))

    #Test negative angles/tolerances
    def test_negative_in_tol_target_above(self):
        self.assertTrue(compare_angles(-90, -180, 120))

    def test_negative_in_tol_given_above(self):
        self.assertTrue(compare_angles(-180, -90, 120))

    def test_neg_tol_in_range(self):
        self.assertTrue(compare_angles(180, 150, -45))

    def test_neg_tol_out_range(self):
        self.assertFalse(compare_angles(180, 150, -15))
