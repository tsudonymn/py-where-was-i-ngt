from datetime import datetime
from typing import List, Optional, TypedDict
import random

class Location(TypedDict):
    latitudeE7: int
    longitudeE7: int
    placeId: str
    address: str
    name: str

class Duration(TypedDict):
    startTimestampMs: str
    endTimestampMs: str

class Waypoint(TypedDict):
    latE7: int
    lngE7: int

class WaypointPath(TypedDict):
    waypoints: List[Waypoint]

class PlaceVisit(TypedDict):
    location: Location
    duration: Duration
    visitConfidence: int

class ActivitySegment(TypedDict):
    startLocation: Location
    endLocation: Location
    duration: Duration
    activityType: str
    confidence: str
    waypointPath: WaypointPath

class TimelineObject(TypedDict):
    placeVisit: Optional[PlaceVisit]
    activitySegment: Optional[ActivitySegment]

class TimelineEntry(TypedDict):
    timelineObjects: List[TimelineObject]

class TimelineData(TypedDict):
    timelineObjects: List[TimelineEntry]

# ... (Location, Duration, Waypoint, WaypointPath, PlaceVisit, ActivitySegment, TimelineObject, TimelineEntry, TimelineData definitions from previous response)

def generate_random_location():
    # Simplified random location generation (for demonstration)
    lat = random.randint(300000000, 500000000)  # Roughly US latitudes
    lng = random.randint(-1200000000, -700000000) # Roughly US longitudes
    return Location(
        latitudeE7=lat,
        longitudeE7=lng,
        placeId=f"ChIJ{random.randint(100000, 999999)}",
        address=f"Random Location {random.randint(1, 100)}",
        name=f"Place {random.randint(1, 50)}"
    )

def generate_random_duration():
    start = 1640995200000 + random.randint(0, 31536000000) # Start from Jan 1, 2022 + up to a year
    end = start + random.randint(3600000, 86400000) # Add between 1 hour and 1 day
    return Duration(startTimestampMs=str(start), endTimestampMs=str(end))

def generate_random_activity():
    activities = ["IN_VEHICLE", "WALKING", "CYCLING", "ON_TRANSIT", "STILL"]
    return random.choice(activities)

def generate_random_confidence():
    confidences = ["HIGH", "MEDIUM", "LOW"]
    return random.choice(confidences)

def generate_random_timeline_object():
    if random.random() < 0.5:  # 50% chance of PlaceVisit
        return TimelineObject(placeVisit=PlaceVisit(location=generate_random_location(), duration=generate_random_duration(), visitConfidence=random.randint(50, 100)), activitySegment=None)
    else:  # 50% chance of ActivitySegment
        start_loc = generate_random_location()
        end_loc = generate_random_location()
        return TimelineObject(
            placeVisit=None,
            activitySegment=ActivitySegment(
                startLocation=start_loc,
                endLocation=end_loc,
                duration=generate_random_duration(),
                activityType=generate_random_activity(),
                confidence=generate_random_confidence(),
                waypointPath=WaypointPath(waypoints=[
                    Waypoint(latE7=start_loc['latitudeE7'], lngE7=start_loc['longitudeE7']),
                    Waypoint(latE7=end_loc['latitudeE7'], lngE7=end_loc['longitudeE7'])
                ])
            )
        )


# Generate 12 records (TimelineEntries)
timeline_data = []
for _ in range(3): # create three different days
    timeline_objects: List[TimelineObject] = []
    for _ in range(4): # create four events per day
        timeline_objects.append(generate_random_timeline_object())
    timeline_data.append(TimelineEntry(timelineObjects=timeline_objects))



# Example access (printing a summary):
for entry in timeline_data:
    print("New Day")
    for obj in entry["timelineObjects"]:
        if obj.get("placeVisit"):
            place_visit = obj["placeVisit"]
            print(f"Visited {place_visit['location']['name']} from {place_visit['duration']['startTimestampMs']} to {place_visit['duration']['endTimestampMs']}")
        elif obj.get("activitySegment"):
            activity = obj["activitySegment"]
            print(f"Traveled by {activity['activityType']} from {activity['startLocation']['latitudeE7']} to {activity['endLocation']['latitudeE7']}")

# You can now easily convert this to JSON using:
import json
print(json.dumps(timeline_data, indent=2))

now = datetime.now()
prefix = 'sample_timeline_data'
timestamp = now.strftime("%Y%m%d_%H%M%S")  # Human-readable timestamp
filename = f"{prefix}_{timestamp}.json"

try:
    with open(filename, "w", encoding="utf-8") as f: # added utf-8 encoding
        json.dump(timeline_data, f, indent=4)  # Use indent for pretty printing
    print(f"Timeline Data written to {filename}")
except OSError as e: # Catching potential OS errors
    print(f"Error writing to file: {e}")
except TypeError as e: # Catching Type errors if data is not JSON serializable
    print(f"Error serializing data to JSON: {e}")