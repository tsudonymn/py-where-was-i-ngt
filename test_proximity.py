import unittest
from proximity import are_points_within_distance, is_location_near_point
from google_timeline_classes import Point as GooglePoint
from my_timeline_classes import Location

class TestProximity(unittest.TestCase):
    def test_points_within_distance(self):
        # Points approximately 1 km apart
        point1 = (40.7128, -74.0060)  # New York
        point2 = (40.7218, -74.0060)  # 1 km north of New York
        self.assertTrue(are_points_within_distance(point1, point2, 1.1))

    def test_points_outside_distance(self):
        # Points approximately 1 km apart
        point1 = (40.7128, -74.0060)  # New York
        point2 = (40.7218, -74.0060)  # 1 km north of New York
        self.assertFalse(are_points_within_distance(point1, point2, 0.9))

    def test_points_at_exact_distance(self):
        # Points approximately 1 km apart
        point1 = (40.7128, -74.0060)  # New York
        point2 = (40.7218, -74.0060)  # 1 km north of New York
        self.assertTrue(are_points_within_distance(point1, point2, 1.0))

    def test_location_near_point(self):
        # Create Location and Point objects with coordinates ~500m apart
        location = Location("place1", "40.7128,-74.0060", "New York")
        point = GooglePoint("40.7178,-74.0060", "2024-01-01T12:00:00.000+00:00")
        self.assertTrue(is_location_near_point(location, point))

    def test_location_far_from_point(self):
        # Create Location and Point objects with coordinates ~2km apart
        location = Location("place1", "40.7128,-74.0060", "New York")
        point = GooglePoint("40.7328,-74.0060", "2024-01-01T12:00:00.000+00:00")
        self.assertFalse(is_location_near_point(location, point))

    def test_location_at_exact_distance(self):
        # Create Location and Point objects with coordinates exactly 1km apart
        location = Location("place1", "40.7128,-74.0060", "New York")
        point = GooglePoint("40.7218,-74.0060", "2024-01-01T12:00:00.000+00:00")
        self.assertTrue(is_location_near_point(location, point))

if __name__ == '__main__':
    unittest.main()