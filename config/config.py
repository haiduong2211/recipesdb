from pymongo import MongoClient

# Define a function to get a MongoDB client
def get_mongo_client(uri="mongodb://localhost:27017", db_name="recipedb_raw"):
    client = MongoClient(uri)
    db = client[db_name]
    return db



