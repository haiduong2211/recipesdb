from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, array, struct, lit, when, split,regexp_replace, to_json
import psycopg2
import os
from utils.convert_json_multiline import convert_multiline_json_to_valid_json
from dotenv import load_dotenv

# Load environment variables from .env file

# Return tables to update to postgresql
def spoonacular_transform():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("Spoonacular Transform and Load") \
        .config("spark.mongodb.read.connection.uri", "mongodb://localhost:27017/recipedb_raw") \
        .config("spark.mongodb.write.connection.uri", "mongodb://localhost:27017/recipedb_raw") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0") \
        .getOrCreate()

    load_dotenv()
    # PostgreSQL connection details from environment variables
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
)
    # Read raw recipes data from MongoDB
    raw_recipes = spark.read.format("mongodb").option("collection", "spoonacular_raw").load()
    default_admin_id = "admin"
    # raw_recipes.printSchema()
    # Explode the extendedIngredients array
    recipe_fact_df = raw_recipes.select(
        #recipe_id is autogenerated
        #user_id is default admin
        #Date is autogenerated
        col('preparationMinutes').alias("prep_time_minutes"),
        col("cookingMinutes").alias("cook_time_minutes"),
        col("readyInMinutes").alias("total_time_minutes"),
        col("title").alias("recipe_name"),
        col("summary").alias("recipe_description"),
        to_json(col("analyzedInstructions")).alias("instruction"),
        col("cuisines").alias("cuisine"),
        col("dishTypes").alias("dish_type"),
        col("occasions").alias("category"),
        col("diets").alias("diet"),
        col("id").alias("source_id"),
        col("sourceUrl").alias("url"),
        col("spoonacularScore").alias("source_score"),
        col("image").alias("image_url"),
        col("servings").alias("servings"),
        col("vegan"),
        col("vegetarian")
    )
    
    ingredients_df = raw_recipes.select(col('id').alias('recipe_id'),explode(col('extendedIngredients')))
    ingredients_df.printSchema()
# Next step. Import converter
spoonacular_transform()
