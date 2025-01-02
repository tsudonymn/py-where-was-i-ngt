import json
from my_timeline_classes import Location
from test_timeline_data_importer import timeline_json_file_name


class Preferences:
    def __init__(self, filepath="preferences.json"):
        self.preferences = load_preferences(filepath)
        self._locations = self.locations()

    def locations(self):
        return self.locations_from_json_string(json.dumps(self.preferences))

    def add_location(self, place_id: str, place_location: str, label: str):
        """
        Adds a location to the preferences.
        """
        self._locations.append({
            'placeId': place_id,
            'placeLocation': place_location,
            'label': label
        })

    def get_locations(self):
        """
        Lazily loads the locations as a dictionary where 'placeId' is the key.
        """
        if self._locations_dict is None:
            # Lazily create the dictionary on first access
            self._locations_dict = {location['placeId']: location for location in self._locations}
        return self._locations_dict

    def locations_from_json_string(self, locations_json):
        """Parses JSON and returns a list of Location objects."""
        try:
            data = json.loads(locations_json)
        except json.JSONDecodeError:
            print("Invalid JSON string.")
            return []

        locations_data = data.get("locations", [])
        locations = []
        for location_data in locations_data:
            location = Location.from_json(location_data)
            if location:  # check if the location was created successfully
                locations.append(location)

        return locations

def load_preferences(filepath="preferences.json"):
    try:
        with open(filepath, "r") as f:
            content = f.read()
            if not content.strip():
                return {"locations": []}
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"locations": []}  # Default preferences with empty locations
