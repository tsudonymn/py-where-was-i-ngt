from datetime import datetime
from typing import List

class Point:
    def __init__(self, point: str, time: str):
        self.point = point
        self.time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z")

class TimelinePath:
    def __init__(self, points: List[Point]):
        self.points = points

class TopCandidate:
    def __init__(self, place_id: str, semantic_type: str, probability: float, place_location: str):
        self.place_id = place_id
        self.semantic_type = semantic_type
        self.probability = probability
        self.place_location = place_location

class Visit:
    def __init__(self, hierarchy_level: int, probability: float, top_candidate: TopCandidate):
        self.hierarchy_level = hierarchy_level
        self.probability = probability
        self.top_candidate = top_candidate

class Activity:
    def __init__(self, start: str, end: str, distance_meters: float, top_candidate: TopCandidate):
        self.start = start
        self.end = end
        self.distance_meters = distance_meters
        self.top_candidate = top_candidate

class SemanticSegment:
    def __init__(self, start_time: str, end_time: str, timeline_path: TimelinePath = None, visit: Visit = None, activity: Activity = None):
        self.start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f%z")
        self.end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%f%z")
        self.timeline_path = timeline_path
        self.visit = visit
        self.activity = activity