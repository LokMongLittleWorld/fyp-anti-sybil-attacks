import os
from sqlalchemy import create_engine, text

# Step 1: Get MySQL connection details from environment variables
db_user = os.environ.get('MYSQL_USER', 'root')
db_password = os.environ.get('MYSQL_PASSWORD', 'root')
db_host = os.environ.get('MYSQL_HOST', 'db')
db_port = os.environ.get('MYSQL_PORT', '3306')
db_name = os.environ.get('MYSQL_DATABASE', 'fyp_web3')
table_name = 'test_table'

# Step 2: Create a MySQL engine connection using SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Step 3: Test the database connection and create a simple table
try:
    with engine.connect() as connection:
        print("Successfully connected to the database!")

        # Step 4: Check if the table exists, and drop it if it does
        result = connection.execute(text(f"SHOW TABLES LIKE '{table_name}';"))
        table_exists = result.fetchone() is not None
        
        if table_exists:
            print(f"Table '{table_name}' exists. Dropping it...")
            connection.execute(text(f"DROP TABLE {table_name};"))
            print(f"Table '{table_name}' dropped successfully.")

        # Step 5: Create a new table
        connection.execute(text(f"""
            CREATE TABLE {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT
            );
        """))
        print(f"Table '{table_name}' created successfully!")

except Exception as e:
    print(f"Error connecting to the database or creating the table: {e}")
