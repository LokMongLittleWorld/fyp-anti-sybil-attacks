import os
import pandas as pd

from utils import load_csv_to_dataframe

# Step 1: Read the CSV into a Pandas DataFrame
csv_file_path = '/app/dataset/eth_std_transactions_10k_lines.csv'
df = load_csv_to_dataframe(csv_file_path)

# Step 2: Extract the functionName column
if 'functionName' in df.columns:
    # Find all unique function names
    unique_function_names = df['functionName'].dropna().unique()

    # Step 3: Display the result
    print("Unique functionName values found:")
    for function_name in unique_function_names:
        print(function_name)

    # Optional: Save the unique function names to a text file
    output_file_path = '/app/result/unique_function_names.txt'
    with open(output_file_path, 'w') as f:
        for function_name in unique_function_names:
            f.write(f"{function_name}\n")
    print(f"Unique function names saved to {output_file_path}")
else:
    print("Error: 'functionName' column not found in the dataset.")
