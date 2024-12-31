# Import the necessary library
import os


# Function to search for a string in a file and print surrounding lines
def search_string_in_file(file_path, search_string, context_lines):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File {file_path} not found")
        return

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Iterate through the lines and search for the string
    for i, line in enumerate(lines):
        if search_string in line:
            start_line = max(0, i - context_lines)
            end_line = min(len(lines) - 1, i + context_lines)
            context = lines[start_line:end_line + 1]

            # Print the context lines
            for context_line in context:
                print(context_line.strip())
            print('')  # Print a blank line between results


# Example usage
file_path = '12192924_Timeline.json'
search_string = 'placeId'
context_lines = 5

search_string_in_file(file_path, search_string, context_lines)
