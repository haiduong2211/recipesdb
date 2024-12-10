from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode
import psycopg2
import os
from utils.convert_json_multiline import convert_multiline_json_to_valid_json
import logging

def spoonacular_transform():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("Spoonacular Transform and Load") \
        .config("spark.mongodb.read.connection.uri", "mongodb://localhost:27017/recipedb_raw") \
        .config("spark.mongodb.write.connection.uri", "mongodb://localhost:27017/recipedb_raw") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0") \
        .getOrCreate()


    # PostgreSQL connection details
    conn = psycopg2.connect(
        host="recipedb-posgresql.c968e6o62c2l.ap-southeast-1.rds.amazonaws.com",
        port=5432,
        database="recipedb",
        user="recipedb_admin",
        password="Hainhu99"
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
