import json
from datetime import datetime
from typing import List, Dict
from google_timeline_classes import SemanticSegment
from my_timeline_classes import Location
from proximity import is_location_near_point


def find_segments_near_location(
    locations: List[Location],
    segments: List[SemanticSegment]
) -> Dict[str, List[SemanticSegment]]:
    """Find semantic segments that are near each location.
    
    Args:
        locations: List of Location objects to check proximity against
        segments: List of SemanticSegment objects to check
        
    Returns:
        Dict mapping location place IDs to lists of nearby semantic segments
    """
    results = {}
    
    for location in locations:
        nearby_segments = []
        for segment in segments:
            if segment.timeline_path:
                for point in segment.timeline_path.points:
                    if is_location_near_point(location, point):
                        nearby_segments.append(segment)
                        break
        
        if nearby_segments:
            results[location.placeId] = nearby_segments
    
    return results


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
