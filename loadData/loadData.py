import os
import pandas as pd
from sqlalchemy import create_engine

# Step 1: Read the CSV into a Pandas DataFrame
csv_file_path = '/app/dataset/eth_std_transactions_10lines.csv'
if not os.path.exists(csv_file_path):
    print(f"Error: File not found at {csv_file_path}")
    print("Current directory:", os.getcwd())
    print("Directory contents:", os.listdir('/app/dataset'))
    exit(1)

df = pd.read_csv(csv_file_path)

# Step 2: Get MySQL connection details from environment variables
db_user = os.environ.get('MYSQL_USER', 'root')
db_password = os.environ.get('MYSQL_PASSWORD', 'root')
db_host = os.environ.get('MYSQL_HOST', 'db')
db_port = os.environ.get('MYSQL_PORT', '3306')
db_name = os.environ.get('MYSQL_DATABASE', 'fyp_web3')
table_name = 'eth_std_transactions'

# Step 3: Create a MySQL engine connection using SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Step 4: Write DataFrame to MySQL (it will create the table if it doesn't exist)
df.to_sql(table_name, con=engine, if_exists='replace', index=False)

print(f"Data loaded into {table_name} successfully!")