import json
from pymongo import MongoClient
import os
'''Load multiple JSON file to mongodb'''

# Specify the directory containing the JSON files
directory = 'data/output/'

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
        with open('config/spoonacularConf.json','r') as f:
            config_data = json.load(f)
            # If the file is existed in imported_file, skip it
            if filename in config_data['imported_file']:
                continue
            else:
            #Add new file name to imported_file
                config_data['imported_file'].append(filename)
                with open('config/spoonacularConf.json', 'w') as f:
                    json.dump(config_data, f)
            # Insert data into MongoDB
                collection.insert_many(data)

# Close the connection
client.close()
