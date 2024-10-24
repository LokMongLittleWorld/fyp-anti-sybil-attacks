import pandas as pd

from utils import load_csv_to_dataframe

# Step 1: Load the bulk_transactions CSV
input_file_path = '/app/result/bulk_transactions.csv'
output_file_path = '/app/result/expend_bulk_transactions.csv'

# Load the DataFrame
bulk_transactions = load_csv_to_dataframe(input_file_path)

# Step 2: Filter the DataFrame for transactions_count > 10
filtered_transactions = bulk_transactions[bulk_transactions['transactions_count'] >= 10]

print('length of filtered_transactions:', len(filtered_transactions))

# Step 3: Expand transfers_list into separate rows
expanded_rows = []

for _ , row in filtered_transactions.iterrows():
    transfers = eval(row['transfers_list'])  # This is a list of tuples (to, value, functionName)
    # sort the transfers by timestamp
    transfers = sorted(transfers, key=lambda x: x[3])
    
    for index, transfer in enumerate(transfers):
        expanded_rows.append({
            'from': row['from'],
            'to': transfer[0],
            # timeGap between each transfer
            'timeGap': transfer[3] - transfers[index-1][3] if index > 0 else 0,
            'value': transfer[1],
            'functionName': transfer[2]
        })

    expanded_rows.append({
            'from': '',
            'to': '',
            'value': '',
            'timeGap': '',
            'functionName': ''
    })

# Create a new DataFrame from the expanded rows
expanded_df = pd.DataFrame(expanded_rows)

# Step 4: Save the new DataFrame to a CSV file
expanded_df.to_csv(output_file_path, index=False)

print(f'Filtered transfers saved to {output_file_path}')
