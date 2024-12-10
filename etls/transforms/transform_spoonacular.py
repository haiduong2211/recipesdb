from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, explode, year, month, dayofmonth, dayofweek
import psycopg2

def spoonacluar_transform():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("Spoonacular Transform and Load") \
        .config("spark.mongodb.read.connection.uri", "mongodb://localhost:27017/") \
        .config("spark.mongodb.read.database", "recipedb_raw") \
        .getOrCreate()

    # PostgreSQL connection details
    conn = psycopg2.connect(
        host="recipedb-posgresql.c968e6o62c2l.ap-southeast-1.rds.amazonaws.com",
        port=5432,
        database="recipedb",
        user="recipedb_admin",
        password="Hainhu99"
    )

    # Load raw data from MongoDB
    raw_recipes = spark.read.format("mongodb").option("collection", "recipes").load()
    raw_ingredients = spark.read.format("mongodb").option("collection", "ingredients").load()

    # -----------------
    # Transform Data
    # -----------------

    # # User_Dim
    # user_dim_df = raw_users.select(
    #     col("id").alias("user_id"),
    #     col("name").alias("user_name"),
    #     col("country"),
    #     col("signup_date")
    # )

    # # Date_Dim
    # date_df = raw_recipes.select(
    #     col("created_date").alias("date")
    # ).distinct()

    # date_dim_df = date_df.withColumn("date_id", col("date").cast("integer")) \
    #     .withColumn("year", year(col("date"))) \
    #     .withColumn("month", month(col("date"))) \
    #     .withColumn("day", dayofmonth(col("date"))) \
    #     .withColumn("day_of_week", dayofweek(col("date"))) \
    #     .withColumn("is_weekend", (col("day_of_week") >= 6).cast("boolean"))

    # Ingredient_Dim
    ingredient_dim_df = raw_ingredients.select(
        col("id").alias("ingredient_id"),
        col("name").alias("ingredient_name"),
        col("category")
    )

    # Recipe_Fact
    recipe_fact_df = raw_recipes.select(
        col("id").alias("recipe_id"),
        col("user_id"),
        col("created_date").alias("date_id"),
        col("rating"),
        col("review_count"),
        col("prep_time_minutes"),
        col("cook_time_minutes"),
        col("total_time_minutes"),
        col("name").alias("recipe_name"),
        col("description").alias("recipe_description"),
        col("instructions").alias("instruction"),
        col("cuisine"),
        col("category"),
        col("source"),
        col("source_id"),
        col("serving"),
        col("vegan"),
        col("vegetarian"),
        col("dish_type")
    )

    # Recipe_Ingredients
    recipe_ingredients_df = raw_recipes.select(
        col("extendedIngredients")
    ).show()


    # # Join Recipe_Ingredients with Ingredient_Dim to get `ingredient_id`
    # recipe_ingredients_final_df = recipe_ingredients_final_df.join(
    #     ingredient_dim_df,
    #     recipe_ingredients_final_df["ingredient_name"] == ingredient_dim_df["ingredient_name"]
    # ).select(
    #     col("recipe_id"),
    #     col("ingredient_id"),
    #     col("unit_of_measure"),
    #     col("quantity")
    # )

    # -----------------
    # Load Data into PostgreSQL
    # -----------------

    # # Function to write DataFrame to PostgreSQL
    # def write_to_postgres(df, table_name):
    #     df.write.jdbc(
    #         url=jdbc_url,
    #         table=table_name,
    #         mode="append",
    #         properties=connection_properties
    #     )

    # # Load data into respective tables
    # write_to_postgres(user_dim_df, "User_Dim")
    # write_to_postgres(date_dim_df, "Date_Dim")
    # write_to_postgres(ingredient_dim_df, "Ingredient_Dim")
    # write_to_postgres(recipe_fact_df, "Recipe_Fact")
    # write_to_postgres(recipe_ingredients_final_df, "Recipe_Ingredients")

    print("Data transformation and loading completed successfully.")
if __name__ == "__main__":
    spoonacluar_transform()