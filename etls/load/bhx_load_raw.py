import sys
import os
# Adjust the path to the utils module
sys.path.append("../..")
from utils.load_to_mongodb import import_json_to_mongodb

# Call the function with the appropriate arguments
import_json_to_mongodb('/Users/duongnguyen/Code/DE_reddit/recipesdb/data/bachhoaxanh/recipes/recipe.json', 'recipedb_raw', 'bachhoaxanh_raw')