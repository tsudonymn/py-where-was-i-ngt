import json
from datetime import datetime

def main():
    print("py-where-was-i analysis beginning!")

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

if __name__ == "__main__":
    main()
