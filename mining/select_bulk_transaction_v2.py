import os
import pandas as pd
from datetime import datetime

class BulkTransactionDetector:
    def __init__(self, time_window_seconds=60):
        """
        Initialize the detector with a specified time window
        :param time_window_seconds: The time window to group transactions (default: 60 seconds)
        """
        self.time_window = time_window_seconds

    def read_data(self, file_path):
        """
        Read the transaction dataset from CSV
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def process_transactions(self, df):
        """
        Process transactions and detect bulk transfers
        """
        # Filter relevant columns
        df_filtered = df[[
            'hash', 'from', 'timeStamp', 'to', 'value', 
            'functionName', 'address'
        ]].copy()

        # Round timestamps to the nearest time window
        df_filtered['timeStamp_rounded'] = (
            df_filtered['timeStamp'] // self.time_window
        ) * self.time_window

        # Create transfers list with additional information
        def create_transfer_list(group):
            transfers = []
            for _, row in group.iterrows():
                transfer = {
                    'address': row['to'] if pd.notna(row['to']) else row['address'],
                    'amount': row['value'],
                    'functionName': row['functionName'] if pd.notna(row['functionName']) else 'transfer'
                }
                transfers.append(transfer)
            return transfers

        # Group transactions
        bulk_transactions = (
            df_filtered
            .groupby(['from', 'timeStamp_rounded'])
            .agg(
                txn_hash=('hash', 'first'),
                timestamp_min=('timeStamp', 'min'),
                duration=('timeStamp', lambda x: x.max() - x.min()),
                transactions_count=('to', 'size'),
                transfers_list=('to', lambda g: create_transfer_list(
                    df_filtered.loc[g.index]
                ))
            )
            .reset_index()
        )

        # Filter for multiple transactions only
        return bulk_transactions[bulk_transactions['transactions_count'] > 1]

    def save_results(self, bulk_transactions, output_path):
        """
        Save results to CSV file
        """
        try:
            bulk_transactions.to_csv(output_path, index=False)
            print(f"Results saved to {output_path}")
        except Exception as e:
            print(f"Error saving results: {e}")

def main():
    # Configuration
    INPUT_FILE = '/app/dataset/eth_std_transactions_10k_lines.csv'
    OUTPUT_FILE = '/app/result/bulk_transactions_10k.csv'
    TIME_WINDOW = 60  # Time window in seconds

    # Initialize detector
    detector = BulkTransactionDetector(time_window_seconds=TIME_WINDOW)

    # Read data
    df = detector.read_data(INPUT_FILE)
    if df is None:
        return

    # Process transactions
    bulk_transactions = detector.process_transactions(df)

    # Print summary
    print("\nBulk Transaction Detection Summary:")
    print(f"Total bulk transactions found: {len(bulk_transactions)}")
    print("\nSample of detected bulk transactions:")
    print(bulk_transactions.head())

    # Save results
    detector.save_results(bulk_transactions, OUTPUT_FILE)

if __name__ == "__main__":
    main()