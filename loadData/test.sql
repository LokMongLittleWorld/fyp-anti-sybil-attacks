-- Switch to the correct database
USE fyp_web3;

-- Create a test table
CREATE TABLE IF NOT EXISTS test_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert a test record
INSERT INTO test_table (name) VALUES ('Test Record');

-- Verify the insertion
SELECT * FROM test_table;

-- Show all tables in the database
SHOW TABLES;

-- If eth_std_transactions table exists, show its structure
SHOW CREATE TABLE eth_std_transactions;

-- Show MySQL version and current user
SELECT VERSION(), USER();

-- Show authentication plugin for root user
SELECT user, host, plugin FROM mysql.user WHERE user='root';