import json
from pymongo import MongoClient
import os
import csv
def load_files_to_mongodb(directory):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cookbookapp']
    collection = db['data']

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            # Load JSON file
            with open(os.path.join(directory, filename)) as file:
                data = json.load(file)
            #{"offset": 3100, "key_no": 1,"imported_file": []}
            with open('/Users/duongnguyen/Code/DE_reddit/recipesdb/config/spoonacularConf.json','r') as f:
                config_data = json.load(f)
                # If the file is existed in imported_file, skip it
                if filename in config_data['imported_file']:
                    continue
                else:
                    # Add new file name to imported_file
                    config_data['imported_file'].append(filename)
                    with open('/Users/duongnguyen/Code/DE_reddit/recipesdb/config/spoonacularConf.json', 'w') as f:
                        json.dump(config_data, f)
                    # Insert data into MongoDB
                    collection.insert_many(data)

    # Close the connection
    client.close()

# # Specify the directory containing the JSON files
# directory = '/Users/duongnguyen/Code/DE_reddit/recipesdb/data/output'

# # Call the function to load files to MongoDB
# load_files_to_mongodb(directory)

def import_csv_to_mongodb(collection, csv_file):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['recipedb_raw']
    collection = db[collection]
    # Open the CSV file
    with open(csv_file, 'r') as file:
        # Read the CSV data
        csv_data = csv.DictReader(file)
        
        # Iterate over each row in the CSV data
        for row in csv_data:
            # Insert the row into MongoDB collection
            collection.insert_one(row)