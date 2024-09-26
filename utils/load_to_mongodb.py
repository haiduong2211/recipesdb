import json
from pymongo import MongoClient
'''Load a JSON file to mongodb'''

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['cookbookapp']
collection = db['data']

# Load JSON file
with open('data/input/demo.json') as file:
    data = json.load(file)

# Insert data into MongoDB
collection.insert_many(data)

# Close the connection
client.close()