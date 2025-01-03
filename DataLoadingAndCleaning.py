import os
import pandas as pd

def process_all_csv_files(folder_path, rows_to_read=50000, output_folder="cleaned_data"):
    """
    Load and clean all CSV files in a folder.
    - Reads exactly the specified number of rows.
    - Cleans the data (fills missing values instead of dropping rows).
    - Saves the cleaned file to a new folder.

    Parameters:
    - folder_path: Path to the folder containing CSV files.
    - rows_to_read: Number of rows to read from each file (default is 50,000).
    - output_folder: Folder where cleaned files will be saved.

    Returns:
    - None
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    print(f"Found {len(csv_files)} CSV files in the folder.")
    
    # Process each CSV file
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        print(f"Processing file: {file_path}")
        
        try:
            # Load exactly the specified number of rows
            data = pd.read_csv(file_path, nrows=rows_to_read, quotechar='"', escapechar='\\')
            
            # Fill missing values instead of dropping rows
            cleaned_data = data.fillna("N/A")  # Replace "N/A" with any placeholder you prefer
            print(f"Data shape after filling missing values: {cleaned_data.shape}")
            
            # Save the cleaned data to a new CSV file
            output_file_path = os.path.join(output_folder, f"cleaned_{csv_file}")
            cleaned_data.to_csv(output_file_path, index=False)
            print(f"Cleaned data saved to: {output_file_path}")
        except Exception as e:
            print(f"Error processing file {csv_file}: {e}")

# Folder containing the CSV files
folder_path = "C:\Project/dft_test_result_2021/test_result_2022"

# Call the function to process all CSV files
process_all_csv_files(folder_path)
