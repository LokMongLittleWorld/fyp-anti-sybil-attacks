# Web3 Anti-sybil-attack

This project aims to detect Sybil attacks in Web3 environments by analyzing transaction data. It uses Python for data processing and MySQL for data storage.

## Project Structure

```
.
├── dataset/
│   ├── eth_polygon_transactions.csv //no include in this repo
│   ├── eth_std_transactions.csv //no include in this repo
│   ├── features_eth_polygon.csv //no include in this repo
│   └── features_eth_std.csv //no include in this repo
├── loadData/
│   ├── load_data.py // load data into database
│   ├── subfile_generator.py // generate subfile from the orginal data file for development
│   └── test_connection.py
├── mining
│   ├── list_all_functionName.py
│   ├── list_bulk_transaction.py
│   ├── select_bulk_transaction.py
│   └── utils.py
├── result
│   ├── bulk_transactions.csv
│   ├── expend_bulk_transactions.csv
│   └── unique_function_names.txt
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Prerequisites

- Docker
- Docker Compose

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LokMongLittleWorld/fyp-anti-sybil-attacks.git
   cd fyp-anti-sybil-attacks
   ```

2. Download transaction
   get the transaction data from [repo](https://huggingface.co/datasets/Poupou/Gitcoin-ODS-Hackhaton-GR15/tree/main) in hugging face

3. Build the Docker containers:
   ```bash
   docker-compose build
   ```

4. Start the Docker containers:
   ```bash
   docker-compose up -d
   ```

5. The application should now be running. You can access the containters.
   - access the application container
   ```bash
   docker-compose exec app bash
   ```
   - access the database container
   ```bash
   docker-compose exec app bash
   ```

6. Stop the Docker containers:
   ```
   docker-compose down
   ```


## Database Setup

### Verifying Database connection

To verify the database connection and loaded data:

1. Access the application container (if not already in it):
   ```bash
   docker-compose exec app bash
   ```

2. Navigate to the loadData directory:
   ```bash
   cd /app/loadData
   ```

3. Run the python script, if nothing went wrong, a table will be created:
   ```bash
   python test_connection.py
   ```

4. Open a new terminal and access the database coantiner:
   ```bash
   docker-compose exec db mysql -u root -p fyp_web3
   ```
   - password can be found in Docker config file

5. Show available tables, a test_table should be created:
   ```sql
   SHOW TABLES;
   ```

### Loading Data

To load data into the MySQL database:

1. Access the application container:
   ```bash
   docker-compose exec app bash
   ```

2. Navigate to the loadData directory:
   ```bash
   cd /app/loadData
   ```

3. Run the data loading script:
   ```bash
   python load_data.py
   ```

## Mining

### Select Bulk Transaction

1. Aggregate Bulk Transactions:
   - Run the script to identify bulk transactions with multiple transfers.
   ```bash
   python bulk_transaction_aggregator.py
   ```

2. Expand Bulk Transactions:
   - Run the script to filter transactions with at least 10 transfers and expand each transfer into separate rows.
   ```bash
   python bulk_transaction_expander.py
   ```

3. View the result:
   - The result can be found in `result/expend_bulk_transactions.csv`
   
## Development

- You can run the `subfile_generator.py` to generate some smaller dataset for code testing.
- To add new Python dependencies, update `requirements.txt` and rebuild the Docker image.

## Troubleshooting

If you encounter any issues:

1. Check Docker container logs:
   ```
   docker-compose logs
   ```

2. Ensure all required files are in the correct locations.
3. Verify that the CSV file paths in `load_data.py` are correct.