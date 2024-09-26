# Web3 Anti-sybil-attack

This project aims to detect Sybil attacks in Web3 environments by analyzing transaction data. It uses Python for data processing and MySQL for data storage.

## Project Structure

```
.
├── dataset/
│   ├── eth_polygon_transactions.csv //no include in this repo
│   ├── eth_std_transactions.csv //no include in this repo
│   ├── eth_std_transactions_10lines.csv //no include in this repo
│   ├── features_eth_polygon.csv //no include in this repo
│   └── features_eth_std.csv
├── loadData/
│   ├── loadData.py
│   ├── start_mysql.sh
│   └── test.sql
├── mysql-config/
│   └── my.cnf
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
   ```
   git clone https://github.com/LokMongLittleWorld/fyp-anti-sybil-attacks.git
   cd fyp-anti-sybil-attacks
   ```

2. download transaction
   get the transaction data from [repo](https://huggingface.co/datasets/Poupou/Gitcoin-ODS-Hackhaton-GR15/tree/main) in hugging face

3. Build and start the Docker containers:
   ```
   docker-compose up --build -d
   ```

4. The application should now be running. You can access the containter.
   access the application container
   ```
   docker-compose exec app bash
   ```

## Usage

### Loading Data

To load data into the MySQL database:

1. Access the application container:
   ```
   docker-compose exec app bash
   ```

2. Navigate to the loadData directory:
   ```
   cd /app/loadData
   ```

3. Run the data loading script:
   ```
   python loadData.py
   ```

### Verifying Database Setup

To verify the database setup and loaded data:

1. Access the application container (if not already in it):
   ```
   docker-compose exec app bash
   ```

2. Navigate to the loadData directory:
   ```
   cd /app/loadData
   ```

3. Run the test SQL script:
   ```
   mysql -h db -uroot -proot fyp_web3 < test.sql
   ```

## Development

- The main data processing script is `loadData/loadData.py`.
- MySQL configuration can be modified in `mysql-config/my.cnf`.
- To add new Python dependencies, update `requirements.txt` and rebuild the Docker image.

## Troubleshooting

If you encounter any issues:

1. Check Docker container logs:
   ```
   docker-compose logs
   ```

2. Ensure all required files are in the correct locations.
3. Verify that the CSV file paths in `loadData.py` are correct.