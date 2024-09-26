#!/bin/bash

# Function to check if MySQL is installed
check_mysql_installed() {
    if command -v mysql >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Start MySQL server
start_mysql() {
    echo "MySQL server is not running."
    echo "Starting MySQL server..."
    
    # Start the MySQL server
    if [ "$(uname)" == "Darwin" ]; then
        # MacOS
        brew services start mysql
    else
        sudo service mysql start
    fi

    # Check if MySQL started successfully
    if mysqladmin ping >/dev/null 2>&1; then
        echo "MySQL server started successfully."
    else
        echo "Failed to start MySQL server."
    fi
}

# Main script execution
if check_mysql_installed; then
    start_mysql
else
    echo "MySQL server is not installed."
    echo "Please install MySQL. You can install it using Homebrew on MacOS with the following command:"
    echo "brew install mysql"
fi
