# from pyspark.sql import SparkSession

# # Create a Spark session
# spark = SparkSession.builder \
#     .appName("MongoDB to PostgreSQL ETL") \
#     .getOrCreate()

# # Read data from MongoDB
# mongo_uri = "mongodb://localhost:27017/mydb.collection"
# df = spark.read.format("mongo").option("uri", mongo_uri).load()

# # Transform the data (replace with your own transformations)
# transformed_df = df.select("column1", "column2", "column3")

# # Write the transformed data to PostgreSQL
# postgres_url = "jdbc:postgresql://localhost:5432/mydb"
# postgres_properties = {
#     "user": "username",
#     "password": "password",
#     "driver": "org.postgresql.Driver"
# }
# transformed_df.write \
#     .mode("overwrite") \
#     .jdbc(postgres_url, "table_name", properties=postgres_properties)

# # Stop the Spark session
# spark.stop()

import pyspark
print(pyspark.__version__)