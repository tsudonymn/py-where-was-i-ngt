from typing import Tuple, Dict, List
from geopy import Point
from geopy.distance import geodesic
from google_timeline_classes import Point as GooglePoint
from my_timeline_classes import Location


def is_location_near_point(location: Location, point: GooglePoint) -> bool:
    """Check if a Location is within 1km of a Google Timeline Point.
    
    Args:
        location (Location): Location object from my_timeline_classes
        point (GooglePoint): Point object from google_timeline_classes
        
    Returns:
        bool: True if location is within 1km of point, False otherwise
    """
    # Extract coordinates from the Location's placeLocation string
    loc_coords = tuple(map(float, location.placeLocation.split(',')))
    
    # Extract coordinates from the Point's point string
    point_coords = tuple(map(float, point.point.split(',')))
    
    return are_points_within_distance(loc_coords, point_coords, 1.0)


def are_points_within_distance(
    point1: Tuple[float, float],
    point2: Tuple[float, float],
    max_distance_km: float
) -> bool:
    """Check if two points are within a specified distance of each other.
    
    Args:
        point1 (Tuple[float, float]): First point as (latitude, longitude)
        point2 (Tuple[float, float]): Second point as (latitude, longitude)
        max_distance_km (float): Maximum allowed distance in kilometers
        
    Returns:
        bool: True if points are within the specified distance, False otherwise
    """
    p1 = Point(point1[0], point1[1])
    p2 = Point(point2[0], point2[1])
    return geodesic(p1, p2).kilometers <= max_distance_km


def check_proximity(self, target: Tuple[float, float], radius_km: float) -> Dict[str, List[bool]]:
    """Check if user was within specified radius of target location for each hour.

    Args:
        target (Tuple[float, float]): Target location as (latitude, longitude)
        radius_km (float): Radius in kilometers to check

    Returns:
        Dict[str, List[bool]]: Dictionary with hours (0-23) as keys and list of True/False
                             values indicating presence within radius
    """
    if self.location_data is None or self.location_data.empty:
        return {}

    target_point = Point(target[0], target[1])
    results = {str(hour): [] for hour in range(24)}

    for idx, row in self.location_data.iterrows():
        hour = str(idx.hour)
        current_point = Point(row['latitude'], row['longitude'])
        distance = geodesic(target_point, current_point).kilometers
        results[hour].append(distance <= radius_km)

    return results