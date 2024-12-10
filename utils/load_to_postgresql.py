import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="your_host",
    port="your_port",
    database="your_database",
    user="your_username",
    password="your_password"
)

# Create a cursor object
cur = conn.cursor()

# Define the SQL query to create a table
create_table_query = '''
    CREATE TABLE IF NOT EXISTS recipes (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        ingredients TEXT,
        instructions TEXT
    )
'''

# Execute the create table query
cur.execute(create_table_query)

# Load transformed data into the table
with open('transformed_data.csv', 'r') as file:
    next(file)  # Skip the header row
    cur.copy_from(file, 'recipes', sep=',')

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()