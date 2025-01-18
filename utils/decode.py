import json

def utf8_decoder(file_path):
    # Read the JSON data from the file
    # Treat the file as binary and decode it as utf-8
    with open(file_path, 'rb') as file:
        json_data = json.load(file)

    # Save the decoded data to the same file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

    # Save the decoded data to a new file
    with open('unique_output.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

    # Print the decoded data
    print(json_data)

# Example usage
file_path = '/Users/duongnguyen/Code/DE_reddit/recipesdb/data/bachhoaxanh/recipes/recipe.json'
utf8_decoder(file_path)