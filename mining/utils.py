import os
import pandas as pd

def load_csv_to_dataframe(csv_file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and loads it into a Pandas DataFrame.
    
    Parameters:
        csv_file_path (str): The file path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the CSV data.
    """
    if not os.path.exists(csv_file_path):
        print(f"Error: File not found at {csv_file_path}")
        print("Current directory:", os.getcwd())
        print("Directory contents:", os.listdir(os.path.dirname(csv_file_path)))
        exit(1)
    
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_file_path)
    return df
