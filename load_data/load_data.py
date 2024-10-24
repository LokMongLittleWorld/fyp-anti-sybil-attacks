import os
import pandas as pd
from sqlalchemy import create_engine, text
import math

# Step 1: Define the CSV file path
csv_file_path = '/app/dataset/eth_std_transactions.csv'
if not os.path.exists(csv_file_path):
    print(f"Error: File not found at {csv_file_path}")
    print("Current directory:", os.getcwd())
    print("Directory contents:", os.listdir('/app/dataset'))
    exit(1)

# Step 2: Get MySQL connection details from environment variables
db_user = os.environ.get('MYSQL_USER', 'root')
db_password = os.environ.get('MYSQL_PASSWORD', 'root')
db_host = os.environ.get('MYSQL_HOST', 'db')
db_port = os.environ.get('MYSQL_PORT', '3306')
db_name = os.environ.get('MYSQL_DATABASE', 'fyp_web3')
table_name = 'eth_std_transactions'

# Step 3: Create a MySQL engine connection using SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Step 4: Check if the table exists, and drop it if it does
with engine.connect() as connection:
    result = connection.execute(text(f"SHOW TABLES LIKE '{table_name}';"))
    table_exists = result.fetchone() is not None
    
    if table_exists:
        print(f"Table '{table_name}' exists. Dropping it...")
        connection.execute(text(f"DROP TABLE {table_name};"))
        print(f"Table '{table_name}' dropped successfully.")

# Step 5: Define chunk size and calculate total chunks
chunksize = 10000  # Define chunk size (10k rows)
total_rows = sum(1 for _ in open(csv_file_path)) - 1  # Subtract 1 for the header
total_chunks = math.ceil(total_rows / chunksize)

print('calculating total rows and total chunks...')
print(f"Total rows: {total_rows}")
print(f"Total chunks: {total_chunks}")

# Step 6: Load and process the CSV file in chunks
for i, chunk in enumerate(pd.read_csv(csv_file_path, chunksize=chunksize)):
    print(f"Processing chunk {i + 1}/{total_chunks}...")

    # Truncate the 'input' column to 10 characters
    chunk['input'] = chunk['input'].str[:10]
    
    # Debug: Find unsigned 64-bit integer columns and convert them
    for column in chunk.columns:
        if chunk[column].dtype == 'uint64':
            print(f"Converting column '{column}' from uint64 to int64")
            chunk[column] = chunk[column].astype('int64')
    
    # Write the chunk to MySQL, appending data
    try:
        chunk.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"Chunk {i + 1}/{total_chunks} loaded into {table_name} successfully!")
    except Exception as e:
        print(f"Error loading chunk {i + 1}/{total_chunks}: {e}")

print(f"All data from {csv_file_path} has been loaded into {table_name} successfully!")
