import os
import json
import logging
from pymongo import MongoClient
def import_spoonacular_to_mongodb():
    # Configure logging
    logging.basicConfig(filename='imported_files_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

    client = MongoClient('mongodb://localhost:27017/')
    db = client['recipedb_raw']
    collection = db['spoonacular_raw']


    # Read JSON files from the specified directory
    directory = 'data/spoonacular/output'
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            print("Working on file: ", file_path)
            with open(file_path, 'r') as file:
                data = json.load(file)
                # data = json.dumps(data, separators=(',', ':'))
                for recipe in data:
                # Ensure the data is a dictionary
                    if isinstance(recipe, dict):
                        # Insert the data into the specified collection
                        collection.insert_one(recipe)
                        # Log the imported file
                        logging.info(f'Imported file: {filename}')
                    else:
                        logging.warning(f'Skipped file (not a dict): {filename}')

    print("Data import complete.")

import_spoonacular_to_mongodb()