
import json

from my_timeline_classes import Location


class LocationRepo:
    def __init__(self, location_json:str):
        locations_list = json.loads(location_json) 
        self.locations = [Location(**loc) for loc in locations_list] 
        self.placeId_dict = {loc.placeId: loc for loc in locations_list}
        self.name_dict = {loc.name: loc for loc in locations_list}