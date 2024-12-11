from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode
import psycopg2
import os
from utils.convert_json_multiline import convert_multiline_json_to_valid_json
import logging
from dotenv import load_dotenv

# Load environment variables from .env file


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

    # Explode the extendedIngredients array
    exploded_ingredients_df = raw_recipes.select(
        col("id").alias("recipe_id"),
        explode(col("extendedIngredients")).alias("ingredient")
    )
    exploded_ingredients_df.show()


    # Select the necessary fields from the exploded array
    ingredient_dim_df = exploded_ingredients_df.select(
        col("recipe_id"),
        col("ingredient.id").alias("ingredient_id"),
        col("ingredient.name").alias("ingredient_name"),
        col("ingredient.aisle").alias("category"),
        col("ingredient.amount").alias("amount"),
        col("ingredient.unit").alias("unit"))
    ingredient_dim_df.show()
spoonacular_transform()
