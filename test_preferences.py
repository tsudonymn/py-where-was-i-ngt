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

        with patch("builtins.open", new_callable=mock_open, read_data=json.dumps(test_data)):
            prefs = Preferences()
            locations = prefs.locations()
            self.assertEqual(len(locations.locations), 2)
            self.assertEqual(locations.locations[0].label, "PARC")
            self.assertEqual(locations.locations[0].placeLocation, "37.468319°, -122.143936°")
            self.assertEqual(locations.locations[0].placeId, "ChIJAAAAABAAAAARYOAlcSt2CHw")
            self.assertEqual(locations.locations[1].label, "Vegas")
            self.assertEqual(locations.locations[1].placeLocation, "36.1716°, -115.1391°")
            self.assertEqual(locations.locations[1].placeId, "ChIJAAAAAABAAAAR4AosrBcexFk")

    def test_locations_empty_file(self):
        with patch("builtins.open", new_callable=mock_open, read_data=""):
            prefs = Preferences()
            locations = prefs.locations()
            self.assertEqual(len(locations.locations), 0)

    def test_locations_invalid_json(self):
        with patch("builtins.open", new_callable=mock_open, read_data="invalid json"):
            prefs = Preferences()
            locations = prefs.locations()
            self.assertEqual(len(locations.locations), 0)

    def test_locations_missing_locations_key(self):
        test_data = """{"other_key": "value"}"""
        with patch("builtins.open", new_callable=mock_open, read_data=test_data):
            prefs = Preferences()
            locations = prefs.locations()
            self.assertEqual(len(locations.locations), 0)

    def test_place_locations_missing_key(self):
        test_data = {"locations": []}
        with patch("builtins.open", new_callable=mock_open, read_data=json.dumps(test_data)):
            prefs = Preferences()
            locations = prefs.locations()
            self.assertEqual(len(locations.locations), 0)


class TestLoadPreferences(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"locations": []}')
    def test_load_preferences_valid(self, mock_file):
        from preferences import load_preferences
        result = load_preferences()
        self.assertEqual(result, {"locations": []})
        mock_file.assert_called_once_with("preferences.json", "r")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_preferences_empty_file(self, mock_file):
        from preferences import load_preferences
        result = load_preferences()
        self.assertEqual(result, {"locations": []})

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_preferences_missing_file(self, mock_file):
        from preferences import load_preferences
        result = load_preferences()
        self.assertEqual(result, {"locations": []})

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_load_preferences_invalid_json(self, mock_file):
        from preferences import load_preferences
        result = load_preferences()
        self.assertEqual(result, {"locations": []})

    @patch("builtins.open", new_callable=mock_open, read_data='{"locations": [{"placeId": "test1"}, {"placeId": "test2"}]}')
    def test_load_preferences_by_place_id(self, mock_file):
        from preferences import load_preferences
        result = load_preferences()
        self.assertEqual(len(result["locations"]), 2)
        self.assertEqual(result["locations"][0]["placeId"], "test1")
        self.assertEqual(result["locations"][1]["placeId"], "test2")


if __name__ == "__main__":
    unittest.main()
