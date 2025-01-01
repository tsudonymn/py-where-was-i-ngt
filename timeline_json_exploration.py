import json

def extract_place_ids(json_data):
    """
    Extracts all 'placeId' values from a JSON structure.

    Args:
        json_data: The JSON data as a Python dictionary or string.

    Returns:
        A list of place IDs. Returns an empty list if no place IDs are found or if there is an error parsing the JSON.
    """
    place_ids = []

    try:
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        else:
            print("Invalid input: Please provide a JSON string or dictionary.")
            return []

        if "semanticSegments" in data and isinstance(data["semanticSegments"], list):
            for segment in data["semanticSegments"]:
                if "visit" in segment and isinstance(segment["visit"], dict):
                    if "topCandidate" in segment["visit"] and isinstance(segment["visit"]["topCandidate"], dict):
                        if "placeId" in segment["visit"]["topCandidate"]:
                            place_ids.append(segment["visit"]["topCandidate"]["placeId"])

    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    return place_ids

# Example usage with your provided JSON snippet:
json_string = """
{
     "semanticSegments": [
          {
               "startTime": "2010-12-01T11:00:00.000-05:00",
               "endTime": "2010-12-01T13:00:00.000-05:00",
               "timelinePath": [
                    {
                         "point": "42.274628°, -83.744944°",
                         "time": "2010-12-01T11:36:00.000-05:00"
                    },
        {
                         "point": "42.284475°, -83.74689°",
                         "time": "2010-12-01T12:00:00.000-05:00"
                    }
               ]
          },
          {
               "startTime": "2010-12-01T11:41:14.000-05:00",
               "endTime": "2010-12-01T11:52:25.000-05:00",
               "startTimeTimezoneUtcOffsetMinutes": -300,
               "endTimeTimezoneUtcOffsetMinutes": -300,
               "visit": {
                    "hierarchyLevel": 0,
                    "probability": 0.4699999988079071,
                    "topCandidate": {
                         "placeId": "ChIJlVNJjT6uPIgRUo9IXToota0",
                         "semanticType": "UNKNOWN",
                         "probability": 0.03407926857471466,
                         "placeLocation": {
                              "latLng": "42.2795528°, -83.7445199°"
                         }
                    }
               }
          },
          {
               "startTime": "2010-12-01T13:00:00.000-05:00",
               "endTime": "2010-12-01T15:00:00.000-05:00",
               "timelinePath": [
        {
                         "point": "42.27411°, -83.745627°",
                         "time": "2010-12-01T14:55:00.000-05:00"
                    }
               ]
          }
     ]
}
"""

if __name__ == "__main__":
    with open('sample_timeline_data_20241227_191600.json') as f:
        timeline_json_data = json.load(f)

    locations = []

    for timeline_object in timeline_json_data[0]['timelineObjects']:
        if 'placeVisit' in timeline_object:
            place_visit = timeline_object['placeVisit']
            location = {
                'latitude': place_visit['location']['latitudeE7'] / 10000000,
                'longitude': place_visit['location']['longitudeE7'] / 10000000,
                'address': place_visit['location']['address'],
                'name': place_visit['location']['name']
            }
            duration = {
                'start_timestamp': datetime.fromtimestamp(int(place_visit['duration']['startTimestampMs']) / 1000),
                'end_timestamp': datetime.fromtimestamp(int(place_visit['duration']['endTimestampMs']) / 1000)
            }
            locations.append({
                'location': location,
                'duration': duration
            })

    for location in locations:
        print(f"Location: {location['location']['name']}")
        print(f"Start Time: {location['duration']['start_timestamp']}")
        print(f"End Time: {location['duration']['end_timestamp']}")
        print()

    with open("12192924_Timeline.json") as f:
        timeline_data = json.load(f)

        place_ids = extract_place_ids(timeline_data)
        # print(place_ids)  # Output: ['ChIJlVNJjT6uPIgRUo9IXToota0']
        place_id_1545 = 'ChIJAAAAAAAAAAARYOAlcSt2CHw'
        filtered_1545 = [id for id in place_ids if id == place_id_1545]
        print(f"Instances of 1545 {len(filtered_1545)}: {filtered_1545}")

        # unique_strings = list(set(place_ids))
        # print(f"There are {len(unique_strings)} places identified")

        # # Example with a dictionary
        # json_dict = json.loads(json_string)
        # place_ids_from_dict = extract_place_ids(json_dict)
        # print(place_ids_from_dict) # Output: ['ChIJlVNJjT6uPIgRUo9IXToota0']
        #
        # # Example with no placeIds
        # no_placeid_json = """{"test": "test"}"""
        # no_placeids = extract_place_ids(no_placeid_json)
        # print(no_placeids) # Output: []
        #
        # # Example with bad json
        # bad_json = """{"test": "test"""
        # bad_json_list = extract_place_ids(bad_json)
        # print(bad_json_list) # Output: []


