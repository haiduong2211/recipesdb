import psycopg2
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

def connect_to_postgresql():
    """
    Connect to the PostgreSQL database and return the connection and cursor objects.
    """
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()
    return conn, cur

def create_table():
    """
    Create the recipes table in the PostgreSQL database.
    """
    # Get the connection and cursor
    conn, cur = connect_to_postgresql()

    # # Define the SQL query to create a table
    # create_table_query = '''
    #     CREATE TABLE IF NOT EXISTS recipes (
    #         id SERIAL PRIMARY KEY,
    #         name VARCHAR(255) NOT NULL,
    #         ingredients TEXT,
    #         instructions TEXT
    #     )
    # '''

    # Execute the create table query
    cur.execute(create_table_query)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

# Call the create_table function
create_table()