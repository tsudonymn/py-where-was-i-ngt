import json
from location_repo import LocationRepo
from my_timeline_classes import Location
from test_timeline_data_importer import timeline_json_file_name


class Preferences:
    def __init__(self, filepath="preferences.json"):
        self.preferences = self._load_preferences_from_json(filepath)
        location_json = self.preferences.get("locations", [])
        self._locations = LocationRepo(location_json)

    def locations(self):
        return self._locations
    
    def _load_preferences_from_json(filepath="preferences.json"):
        try:
            with open(filepath, "r") as f:
                content = f.read()
                if not content.strip():
                    return {"locations": []}
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"locations": []}  # Default preferences with empty locations
