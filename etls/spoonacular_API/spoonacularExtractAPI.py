import requests
import json
import os
from dotenv import load_dotenv
def spoonacular_API_extract():
    #Load key No from the config file
    with open('config/spoonacularConf.json') as f:
        try:
            config_data = json.load(f)
            key_no = config_data.get('key_no', 0)
        except json.JSONDecodeError:
            key_no = 0
    #Load the Spoonacular API key from the .env file
    print(f"Current key_no: {key_no}")
    load_dotenv()
    api_key = os.getenv(f'SPOONARCULAR_API_KEY_{key_no}')
    
    if api_key == None:
        print("No Remain API key")
        return 

    # Read the offset data from config.json
    with open('config/spoonacularConf.json') as f:
        try:
            config_data = json.load(f)
            offset = config_data.get('offset', 1)
        except json.JSONDecodeError:
            offset = 1
    # Part 0: Parameters
    number = 100 # The number of recipes to retrieve 1-100
    query = ""   #The query to search for
    url = f'https://api.spoonacular.com/recipes/complexSearch?query={query}&number={number}&offset={offset}&addRecipeInformation=true&addRecipeInstructions=true&addRecipeNutrition=true&fillIngredients=true&apiKey={api_key}'

    # Make the request to the Spoonacular API
    response = requests.get(url)
    print(url)
    # Check if the request was successful
    if response.status_code == 402:
        print("API limit reached. Please try again later.")
        #Update to the next key
        key_no += 1
        #Update the key_no in config.json
        config_data['key_no'] = key_no
        with open('config/spoonacularConf.json', 'w') as f:
            json.dump(config_data, f)
        return spoonacular_API_extract()
    elif response.status_code == 401:
        print("No More authorized API key")
        #Update to the next key
        key_no = 1
        return
    print(f"Status code: {response.status_code}")


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
    print(f"New offset: {new_offset}")
    print(f"Data saved to {new_file_name}")
    spoonacular_API_extract()

if __name__ == "__main__":
    spoonacular_API_extract()