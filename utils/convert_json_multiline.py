import json

def convert_multiline_json_to_valid_json(input_file_path, output_file_path):
    # Read the multiline JSON string from the input file
    with open(input_file_path, 'r') as file:
        multiline_json_str = file.read()
    
    # Ensure the multiline JSON string is properly formatted
    # Split the string into individual JSON objects
    json_objects = multiline_json_str.split('}, {')
    
    # Add brackets to each JSON object and fix the formatting
    json_objects = ['{' + obj + '}' if not obj.startswith('{') else obj for obj in json_objects]
    json_objects = [obj + '}' if not obj.endswith('}') else obj for obj in json_objects]
    
    # Join the JSON objects into a valid JSON array
    valid_json_str = '[' + ','.join(json_objects) + ']'
    
    # Parse the JSON string
    try:
        json_data = json.loads(valid_json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    
    # Write the parsed JSON to a file
    with open(output_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

# # Example usage
# input_file_path = 'path/to/multiline_json.txt'
# output_file_path = 'valid_recipes.json'

# convert_multiline_json_to_valid_json(input_file_path, output_file_path)