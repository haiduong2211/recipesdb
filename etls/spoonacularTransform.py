from pymongo import MongoClient


def connect_to_mongodb(database_name = "cookbookapp"):
    # MongoDB connection details
    client = MongoClient("mongodb://localhost:27017/")
    db = client[database_name]  # Replace with your database name
    return db


def get_or_create_ingredient(db,ingredient):
    """
    Check if the ingredient exists, if not, insert and return the id.
    """
    existing_ingredient = db.ingredients.find_one({"name": ingredient["name"]})
    
    if existing_ingredient:
        # If the ingredient already exists, return the _id
        return existing_ingredient["_id"]
    else:
        # Insert the new ingredient and return the new _id
        ingredient_id = db.ingredients.insert_one({
            "spoonacular_id": ingredient["id"],
            "name": ingredient["name"],
            # "nameClean": ingredient.get("nameClean", ""),
            # "original": ingredient.get("original", ""),
            # "originalName": ingredient.get("originalName", ""),
            # "amount": ingredient.get("amount"),
            # "unit": ingredient.get("unit"),
            "aisle": ingredient.get("aisle"),
            # "meta": ingredient.get("meta", []),
            # "measures": ingredient.get("measures", {})
        }).inserted_id
        return ingredient_id


def transform_data(db):
    # Load the data from the 'data' collection
    data_collection = db.data.find()
    current_recipes = db.recipes.count_documents({})
    skipped_recipes = 0
    process_count = 0
    current_ingredients = db.ingredients.count_documents({})
    for recipe in data_collection:
        process_count += 1
        #check if the recipe is in the database
        try:
            existing_recipe = db.recipes.find_one({"spoonacular_id": recipe["id"]})
            if existing_recipe:
                print(f"Recipe {recipe['name']} already exists in the database.")
                skipped_recipes += 1
                continue
        except:
            pass
        # Create an empty list for ingredients that will be embedded in the recipe document
        ingredients_list = []
        
        # Process and deduplicate ingredients
        for ingredient in recipe.get("extendedIngredients", []):
            ingredient_id = get_or_create_ingredient(db,ingredient)

            # Add the ingredient details to the ingredients list, including recipe-specific amount and unit
            ingredients_list.append({
                "ingredientId": ingredient_id,  # Optional, or just use the name
                "name": ingredient["name"],
                "nameClean": ingredient.get("nameClean", ""),
                "consistency": ingredient.get("consistency", ""),
                "original": ingredient.get("original", ""),
                "originalName": ingredient.get("originalName", ""),
                "meta": ingredient.get("meta", []),
                "amount": ingredient.get("amount", None),
                "unit": ingredient.get("unit", ""),
                "measures": ingredient.get("measures", {}),
            })

        # 1. Insert data into 'recipes' collection
        recipe_id = db.recipes.insert_one({
            "spoonacular_id": recipe["id"],
            "title": recipe["title"],
            "readyInMinutes": recipe.get("readyInMinutes", None),
            "servings": recipe.get("servings", None),
            "vegetarian": recipe.get("vegetarian", False),
            "vegan": recipe.get("vegan", False),
            "glutenFree": recipe.get("glutenFree", False),
            "dairyFree": recipe.get("dairyFree", False),
            "veryHealthy": recipe.get("veryHealthy", False),
            "cheap": recipe.get("cheap", False),
            "veryPopular": recipe.get("veryPopular", False),
            "weightWatcherSmartPoints": recipe.get("weightWatcherSmartPoints", None),
            "pricePerServing": recipe.get("pricePerServing", None),
            "spoonacularScore": recipe.get("spoonacularScore", None),
            "sourceUrl": recipe.get("sourceUrl", ""),
            "cuisines": recipe.get("cuisines", []),
            "dishTypes": recipe.get("dishTypes", []),
            "ingredients": ingredients_list,
            "instructions": recipe.get("instructions", []),
        }).inserted_id

        # 3. Insert nutritional information into 'nutrition' collection
        if "nutrition" in recipe:
            db.nutrition.insert_one({
                "recipeId": recipe_id,
                "nutrients": recipe.get("nutrition",{})
            })

    # Tracking Changes  
    print("\n============== CHANGES ============")
    print("Recipes skipped:", skipped_recipes)
    print(f"New recipes added:", db.recipes.count_documents({}) - current_recipes)
    print(f"New Ingredients added:", db.ingredients.count_documents({}) - current_ingredients)
    print('process_count:', process_count)
    #analyze the data
    print("\n============== TOTAL COUNT ============")
    print(f"Total number of recipes: {db.recipes.count_documents({})}")
    print(f"Total number of ingredients: {db.ingredients.count_documents({})}")
    print(f"Total number of nutritional information: {db.nutrition.count_documents({})}")
    print("\n=========================================")
    print("Data transformation completed.")
    print("=========================================")


if __name__ == "__main__":
    db = connect_to_mongodb()
    transform_data(db)
