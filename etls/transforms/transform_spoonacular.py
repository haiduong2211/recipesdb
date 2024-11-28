import requests
import json

def transform_spoonacular(data):
    # Your transformation logic goes here
    transformed_data = []

    # Example transformation: Extracting recipe names
    for recipe in data:
        recipe_name = recipe.get('name')
        transformed_data.append(recipe_name)

