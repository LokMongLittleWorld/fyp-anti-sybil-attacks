import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from utils import load_csv_to_dataframe

input_file_path = '/app/dataset/eth_std_transactions.csv'
output_file_path = '/app/local_result/bulk_transactions.csv'

# Step 1: Read the CSV into a Pandas DataFrame
df = load_csv_to_dataframe(input_file_path)

df['value'] = pd.to_numeric(df['value'], errors='coerce')

# Step 2: Filter only relevant columns and transactions with value > 0
df_filtered = df[['hash', 'from', 'timeStamp', 'to', 'value', 'functionName']]
df_filtered = df_filtered[(df_filtered['value'] > 0)]

# Step 3: Filter for specific function names indicating transfers
transfer_functions = ['Transfer', 'transferFrom', 'batchTransfer', 'bulkTransfer']
df_filtered = df_filtered[df_filtered['functionName'].str.contains('|'.join(transfer_functions), case=False, na=False)]
print ('length of df_filtered:', len(df_filtered))


# Step 4: Round the timestamp to the nearest minute
#df_filtered['timeStamp_rounded'] = (df_filtered['timeStamp'] // 60) * 60  # Round to nearest minute

# Step 5: Group by sender and rounded timestamp, then aggregate transfers
bulk_transactions = (
    df_filtered
    .groupby(['from'])
    .agg(
        txn_hash=('hash', 'first'),  # Store the first transaction hash
        timestamp_min=('timeStamp', 'min'),  # Store the minimum timestamp
        duration=('timeStamp', lambda x: (x.max() - x.min())),  # Calculate duration in seconds
        transactions_count=('to', 'size'),  # Count of transactions
        transfers_list=('to', lambda x: list(zip(x, df_filtered.loc[x.index, 'value'], df_filtered.loc[x.index, 'functionName'], df_filtered.loc[x.index, 'timeStamp']))),  # List of transfers (to, value, timestamp)
        timestamp_gap=('timeStamp', lambda x: list(x- x.min()))  # List of timestamps
    )
    .reset_index()
)

#sort the timestamp gap
bulk_transactions['timestamp_gap'] = bulk_transactions['timestamp_gap'].apply(lambda x: sorted(x))
#calculate the median of the timestamp gap
bulk_transactions['timestamp_gap_median'] = bulk_transactions['timestamp_gap'].apply(lambda x: np.median(x))

print( 'length of bulk_transactions:', len(bulk_transactions))

# Step 6: Filter only bulk transactions (more than one transfer)
bulk_transactions = bulk_transactions[bulk_transactions['transactions_count'] > 1]

# Step 7: Sort the result
bulk_transactions = bulk_transactions.sort_values(by=['transactions_count', 'timestamp_gap_median'], ascending=[False, True])

new_column_order = ['from', 'transactions_count', 'timestamp_gap_median', 'timestamp_gap', 'timestamp_min', 'duration', 'txn_hash','transfers_list']
bulk_transactions = bulk_transactions[new_column_order]

# Optional: Save to a new CSV file
bulk_transactions.to_csv(output_file_path, index=False)
