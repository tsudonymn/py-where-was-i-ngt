import json
from datetime import datetime
from pprint import pprint
from typing import List, Dict
from google_timeline_classes import SemanticSegment
from my_timeline_classes import Location
from preferences import Preferences
from proximity import is_location_near_point
from timeline_importer import load_timeline_data
from icecream import ic


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

    prefs = Preferences()
    locations = prefs.locations()
    semantic_segments = load_timeline_data("12192924_Timeline.json")

    results_dict = find_segments_near_location(locations, semantic_segments)

    pprint("Results:")
    for key in results_dict.keys():
        pprint(f"{key} found {len(results_dict[key])} segments")

    ic(results_dict)

if __name__ == "__main__":
    main()
