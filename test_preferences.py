import json
import unittest
from unittest.mock import patch, mock_open
from preferences import Preferences


class TestPreferences(unittest.TestCase):
    def setUp(self):
        self.prefs = Preferences()

    def test_locations_valid_data(self):
        test_data = {
            "locations": [
                {
                    "placeId": "ChIJAAAAABAAAAARYOAlcSt2CHw",
                    "placeLocation": "37.468319°, -122.143936°",
                    "label": "PARC"
                },
                {
                    "placeId": "ChIJAAAAAABAAAAR4AosrBcexFk",
                    "placeLocation": "36.1716°, -115.1391°",
                    "label": "Vegas"
                }
            ]
        }

        print(f"yuioyuio {test_data}")

        locations = self.prefs.locations_from_string(json.dumps(test_data))
        self.assertEqual(len(locations), 2)
        self.assertEqual(locations[0].label, "PARC")
        self.assertEqual(locations[0].placeLocation, "37.468319°, -122.143936°")
        self.assertEqual(locations[0].placeId, "ChIJAAAAABAAAAARYOAlcSt2CHw")
        self.assertEqual(locations[1].label, "Vegas")
        self.assertEqual(locations[1].placeLocation, "36.1716°, -115.1391°")
        self.assertEqual(locations[1].placeId, "ChIJAAAAAABAAAAR4AosrBcexFk")

    def test_locations_empty_file(self):
        locations = self.prefs.locations_from_string("")
        self.assertEqual(len(locations), 0)

    def test_locations_invalid_json(self):
        locations = self.prefs.locations_from_string("invalid json")
        self.assertEqual(len(locations), 0)

    def test_locations_missing_locations_key(self):
        test_data = """{"other_key": "value"}"""
        locations = self.prefs.locations_from_string(test_data)
        self.assertEqual(len(locations), 0)

    def test_place_locations_missing_key(self):
        test_data = {"locations": []}
        place_locations = self.prefs.locations_from_string(json.dumps(test_data))
        self.assertEqual(len(place_locations), 0)


if __name__ == "__main__":
    unittest.main()
