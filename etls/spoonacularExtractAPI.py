import requests
import json
import os
from dotenv import load_dotenv
import datetime
# Load the Spoonacular API key from the .env file
load_dotenv()

api_key = os.getenv('SPOONARCULAR_API_KEY')
print(api_key)
# Read the offset data from config.json
with open('config/spoonacularConf.json') as f:
    try:
        config_data = json.load(f)
        offset = config_data.get('offset', 0)
    except json.JSONDecodeError:
        offset = 0
# Set the query and other parameters
number = 100
query = ""      # Number of results to return



# Send GET request to the Spoonacular API
# url = f'https://api.spoonacular.com/food/ingredients/search?query={query}&cuisine={cuisine}&number={number}&offset={offset}&apiKey={api_key}'

url = f'https://api.spoonacular.com/recipes/complexSearch?query={query}&number={number}&offset={offset}&addRecipeInformation=true&addRecipeInstructions=true&addRecipeNutrition=true&fillIngredients=true&apiKey={api_key}'


response = requests.get(url)
print(response.url)
# Check if the request was successful
if response.status_code == 200:
    # Get the recipe information from the response
    recipes = response.json()['results']
    count = response.json()['totalResults']
    
    # Calculate the new offset value
    new_offset = offset + number       
    # Update the offset value in config.json
    config_data['offset'] = new_offset
    with open('config/spoonacularConf.json', 'w') as f:
        json.dump(config_data, f)

    # Add the recipes to the json file
    new_file_name  = f'data/output/recipes_{new_offset-100}.json'
    with open(new_file_name, 'w') as f:
        json.dump(recipes, f)
    print(f"Retrieved {len(recipes)} recipes. \n Current Offset: {offset}\n Total recipes: {count}.")
else:
    print(f"Failed to retrieve ingredients. Status code: {response.status_code}")