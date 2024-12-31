from typing import Tuple, Dict, List
from geopy import Point
from geopy.distance import geodesic


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