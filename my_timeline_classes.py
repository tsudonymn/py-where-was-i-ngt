class Location:
    def __init__(self, place_id: str, place_location: str, label: str):
        self.placeId = place_id
        self.placeLocation = place_location
        self.label = label

    @staticmethod
    def from_json(location_json: list):
        return Location(
                place_id=location_json["placeId"],
                place_location=location_json["placeLocation"],
                label=location_json["label"]
            )

        # locations = []
        # for loc in location_json:
        #     new_loc = Location(
        #         place_id=location_json["placeId"],
        #         place_location=location_json["placeLocation"],
        #         label=location_json["label"]
        #     )
        #     locations.append(new_loc)
        # return locations
