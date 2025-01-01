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

    def in_year(self, year: int) -> bool:
        """Check if this segment has any point in the given year"""
        if self.timeline_path and self.timeline_path.points:
            return any(point.time.year == year for point in self.timeline_path.points)
        return self.start_time.year == year or self.end_time.year == year

    @staticmethod
    def filter_by_year(segments: List['SemanticSegment'], year: int) -> List['SemanticSegment']:
        """Filter a list of semantic segments to only those in the given year"""
        return [segment for segment in segments if segment.in_year(year)]

    def __repr__(self) -> str:
        """Human-readable representation of the semantic segment"""
        segment_type = "Visit" if self.visit else "Activity" if self.activity else "Unknown"
        path_info = f" with {len(self.timeline_path.points)} points" if self.timeline_path else ""
        return (f"<SemanticSegment {segment_type}{path_info} "
                f"({self.start_time.strftime('%Y-%m-%d %H:%M')} to "
                f"{self.end_time.strftime('%Y-%m-%d %H:%M')})>")
