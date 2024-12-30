import json

def count_points(data):
    """Counts the number of 'point' values using a list comprehension."""
    try:
        return sum(1 for segment in data.get("semanticSegments", [])
                   for path in segment.get("timelinePath", [])
                   if "point" in path)
    except AttributeError: #handles if data is None
        return 0

# Example usage (replace with your JSON data):
timeline_json_file_name = './12192924_Timeline.json'

with open(timeline_json_file_name, 'r') as file:
    try:
        data = json.load(file)
        total_points = count_points(data)
        print(f"Total Points: {total_points}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")