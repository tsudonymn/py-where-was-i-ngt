import sample_data
import json

# Generate the data
timeline_data = sample_data.timeline_data

# Write the data to a variable
data = json.dumps(timeline_data, indent=2)

# Print the data
print(data)