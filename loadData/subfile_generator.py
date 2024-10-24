import os

# Function to create subfiles by reading the CSV line-by-line
def create_subfiles(input_file_path, output_directory, original_file_name, row_counts):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Open the input file for reading
    with open(input_file_path, 'r') as infile:
        header = infile.readline()  # Read the header line

        # Initialize the starting row index
        start_row = 0

        for n in row_counts:
            # Construct the output file name
            output_file_name = f"{original_file_name}_{n // 1000}k.csv"
            output_file_path = os.path.join(output_directory, output_file_name)

            with open(output_file_path, 'w') as outfile:
                outfile.write(header)  # Write the header to the new file

                # Write 'n' lines to the new file
                for _ in range(n):
                    line = infile.readline()
                    if not line:
                        print(f"No more data available to write for {n} rows.")
                        return
                    outfile.write(line)

            start_row += n
            print(f"Created file: {output_file_path}")

# Main function to run the script
def main():
    original_file_name = 'eth_std_transactions'
    input_file_path = f'/app/dataset/{original_file_name}.csv'
    output_directory = '/app/dataset/'

    # Define the row counts for subfiles
    row_counts = [1000, 10000, 50000, 100000]

    # Create subfiles
    create_subfiles(input_file_path, output_directory, original_file_name, row_counts)

if __name__ == "__main__":
    main()