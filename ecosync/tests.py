# myapp/tests.py
from django.test import TestCase
from .utils import aws_map_route_api

class UtilsTestCase(TestCase):
    def test_aws_map_route_api(self):
        # Sample input data
        source_lat = 24.375389
        source_lon = 88.602569
        dest_lat = 24.377813
        dest_lon = 88.567937
        OptimizeFor = 'FastestRoute'

        # Call the function
        result = aws_map_route_api(source_lat, source_lon, dest_lat, dest_lon, OptimizeFor)

        # Print the result for debugging
        print("Result:", result)
        # Accessing values by their keys
        drive_distance = result['DriveDistance']
        distance_unit = result['DistanceUnit']
        drive_time = result['DriveTime']
        time_unit = result['TimeUnit']
        path_list = result['PathList']

        # Printing the values
        print("Drive Distance:", drive_distance)
        print("Distance Unit:", distance_unit)
        print("Drive Time:", drive_time)
        print("Time Unit:", time_unit)
        print("Path List:", path_list)

        # Assert that the result is a dictionary
        self.assertIsInstance(result, dict)

        # Check if the result contains expected keys
        self.assertIn('DriveDistance', result)
        self.assertIn('DistanceUnit', result)
        self.assertIn('DriveTime', result)
        self.assertIn('TimeUnit', result)

        # If ValidationException is present, print it for debugging
        if 'ValidationException' in result:
            print("Validation Exception:", result['ValidationException'])
        else:
            # Check if 'PathList' key is present
            self.assertIn('PathList', result)
