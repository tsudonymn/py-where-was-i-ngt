import unittest
import json
from timeline_classes import SemanticSegment, Point, TimelinePath, TopCandidate, Visit, Activity

timeline_json_file_name = './12192924_Timeline.json'

class TestTimelineImport(unittest.TestCase):
    def test_import_timeline_json(self):
        with open(timeline_json_file_name, 'r') as file:
            data = json.load(file)

        self.assertIsInstance(data, dict)
        self.assertIn('semanticSegments', data)

    def test_import_semantic_segments(self):
        with open(timeline_json_file_name, 'r') as file:
            data = json.load(file)

        # Check if 'semanticSegments' is present and is a list
        self.assertIn('semanticSegments', data)
        self.assertIsInstance(data['semanticSegments'], list)

        # Check if the first segment has the expected keys
        if data['semanticSegments']:
            first_segment = data['semanticSegments'][0]
            self.assertIn('startTime', first_segment)
            self.assertIn('endTime', first_segment)

    def test_import_semantic_segments_with_classes(self):
        with open(timeline_json_file_name, 'r') as file:
            data = json.load(file)

        semantic_segments = data['semanticSegments']

        # Create a list to store the parsed semantic segments
        parsed_segments = []
        total_timeline_points = 0
        total_visits = 0

        # Iterate over the semantic segments and parse them using the 'SemanticSegment' class
        for segment in semantic_segments:
            start_time = segment['startTime']
            end_time = segment['endTime']
            
            timeline_path = None
            if 'timelinePath' in segment:
                points = [Point(point['point'], point['time']) for point in segment['timelinePath']]
                timeline_path = TimelinePath(points)
                total_timeline_points += len(points)
            
            visit = None
            if 'visit' in segment:
                top_candidate = TopCandidate(
                    segment['visit']['topCandidate']['placeId'],
                    segment['visit']['topCandidate']['semanticType'],
                    segment['visit']['topCandidate']['probability'],
                    segment['visit']['topCandidate']['placeLocation']
                )
                visit = Visit(
                    segment['visit']['hierarchyLevel'],
                    segment['visit']['probability'],
                    top_candidate
                )
                total_visits += 1

            parsed_segment = SemanticSegment(start_time, end_time, timeline_path, visit)
            parsed_segments.append(parsed_segment)

        # Assert that the number of parsed semantic segments is equal to the number of semantic segments in the JSON data
        self.assertEqual(len(parsed_segments), len(semantic_segments))
        
        # Print the counts for verification
        print(f"\nTotal semantic segments: {len(parsed_segments)}")
        print(f"Total timeline points: {total_timeline_points}")
        print(f"Total visits: {total_visits}")

if __name__ == '__main__':
    unittest.main()