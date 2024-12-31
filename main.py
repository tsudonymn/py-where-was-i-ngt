import pandas as pd
from datetime import datetime, timedelta
from google_timeline_classes import SemanticSegment
from preferences import Preferences
from my_timeline_classes import Location
from timeline_importer import load_timeline_data

def produce_report(locations: list[Location], timeline_data: list[SemanticSegment]):
    # Get date range from timeline data
    start_date = min(segment.start_time for segment in timeline_data)
    end_date = max(segment.end_time for segment in timeline_data)
    
    # Create hourly time range
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Create DataFrame with hours as index and locations as columns
    df = pd.DataFrame(index=date_range, columns=[loc.label for loc in locations])
    df[:] = 0  # Initialize all values to 0
    
    # Populate DataFrame with timeline data
    for segment in timeline_data:
        # Get the location label if this segment has a visit
        if segment.visit:
            location_label = segment.visit.top_candidate.place_id
            
            # Find matching location
            for loc in locations:
                if loc.placeId == location_label:
                    # Mark each hour in the segment as 1
                    segment_range = pd.date_range(
                        start=segment.start_time,
                        end=segment.end_time,
                        freq='H'
                    )
                    df.loc[segment_range, loc.label] = 1
    
    return df


if __name__ == "__main__":
    print("py-where-was-i main  beginning!")
    prefs = Preferences()
    locations = prefs.locations()
    semantic_segments = load_timeline_data("12192924_Timeline.json")
    report = produce_report(locations, semantic_segments)
    print(report)