import unittest
from location_analyzer import find_segments_near_location
from google_timeline_classes import Point, TimelinePath, SemanticSegment
from my_timeline_classes import Location

class TestLocationAnalyzer(unittest.TestCase):
    def test_find_segments_near_location(self):
        # Create test locations
        location1 = Location("place1", "40.7128,-74.0060", "New York")
        location2 = Location("place2", "34.0522,-118.2437", "Los Angeles")
        
        # Create test semantic segments with points
        point1 = Point("40.7128,-74.0060", "2024-01-01T12:00:00.000+00:00")  # Near location1
        point2 = Point("40.7178,-74.0060", "2024-01-01T12:05:00.000+00:00")  # Near location1
        point3 = Point("34.0522,-118.2437", "2024-01-01T12:10:00.000+00:00")  # Near location2
        point4 = Point("51.5074,-0.1278", "2024-01-01T12:15:00.000+00:00")  # Far from both
        
        segment1 = SemanticSegment(
            "2024-01-01T12:00:00.000+00:00",
            "2024-01-01T12:10:00.000+00:00",
            timeline_path=TimelinePath([point1, point2])
        )
        segment2 = SemanticSegment(
            "2024-01-01T12:10:00.000+00:00",
            "2024-01-01T12:20:00.000+00:00",
            timeline_path=TimelinePath([point3])
        )
        segment3 = SemanticSegment(
            "2024-01-01T12:20:00.000+00:00",
            "2024-01-01T12:30:00.000+00:00",
            timeline_path=TimelinePath([point4])
        )
        
        # Call function
        result = find_segments_near_location(
            [location1, location2],
            [segment1, segment2, segment3]
        )
        
        # Verify results
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result["place1"]), 1)  # segment1
        self.assertEqual(len(result["place2"]), 1)  # segment2
        self.assertEqual(result["place1"][0], segment1)
        self.assertEqual(result["place2"][0], segment2)

if __name__ == '__main__':
    unittest.main()