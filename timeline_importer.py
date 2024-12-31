from google_timeline_classes import SemanticSegment, TimelinePath, Point, Visit, TopCandidate, Activity
import json

def load_timeline_data(file_path: str) -> list[SemanticSegment]:
    """Load timeline data from JSON file and return list of SemanticSegments"""
    with open(file_path) as f:
        data = json.load(f)
    
    segments = []
    for segment_data in data['semanticSegments']:
        # Convert timeline path if present
        timeline_path = None
        if 'timelinePath' in segment_data:
            points = [Point(point['point'], point['time']) 
                     for point in segment_data['timelinePath']]
            timeline_path = TimelinePath(points)
        
        # Convert visit if present
        visit = None
        if 'visit' in segment_data:
            visit_data = segment_data['visit']
            top_candidate = TopCandidate(
                visit_data['topCandidate']['placeId'],
                visit_data['topCandidate']['semanticType'],
                visit_data['topCandidate']['probability'],
                visit_data['topCandidate']['placeLocation']['latLng']
            )
            visit = Visit(
                visit_data['hierarchyLevel'],
                visit_data['probability'],
                top_candidate
            )
        
        # Convert activity if present
        activity = None
        if 'activity' in segment_data:
            activity_data = segment_data['activity']
            top_candidate = TopCandidate(
                activity_data['topCandidate'].get('placeId', ''),
                activity_data['topCandidate'].get('semanticType', ''),
                activity_data['topCandidate'].get('probability', 0),
                activity_data['topCandidate'].get('placeLocation', {}).get('latLng', '')
            )
            activity = Activity(
                activity_data['start']['latLng'],
                activity_data['end']['latLng'],
                activity_data['distanceMeters'],
                top_candidate
            )
        
        # Create SemanticSegment
        segment = SemanticSegment(
            segment_data['startTime'],
            segment_data['endTime'],
            timeline_path,
            visit,
            activity
        )
        segments.append(segment)
    
    return segments

# Example usage:
# segments = load_timeline_data('sample_timeline_data_20241227_191600.json')
# produce_report(segments)