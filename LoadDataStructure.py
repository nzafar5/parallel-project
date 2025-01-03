import os
import pandas as pd
import numpy as np
from datetime import datetime

def load_and_validate_data(folder_path):
    """
    Load cleaned data and perform additional validation and analysis.
    
    Parameters:
    - folder_path: Path to the folder containing cleaned CSV files
    
    Returns:
    - Combined and validated DataFrame
    """
    # Load the cleaned data
    df = load_cleaned_data(folder_path)
    
    # Additional validation steps
    df = validate_dates(df)
    df = validate_numeric_columns(df)
    df = standardize_categorical_columns(df)
    
    return df

def validate_dates(df):
    """Validate and standardize date columns"""
    if 'test_date' in df.columns:
        df['test_date'] = pd.to_datetime(df['test_date'], errors='coerce')
    if 'first_use_date' in df.columns:
        df['first_use_date'] = pd.to_datetime(df['first_use_date'], errors='coerce')
    return df

def validate_numeric_columns(df):
    """Validate and clean numeric columns"""
    numeric_validations = {
        'test_mileage': (0, 1000000),
        'cylinder_capacity': (0, 10000),
        'test_class_id': (1, 7)
    }
    
    for column, (min_val, max_val) in numeric_validations.items():
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
            mask = (df[column] < min_val) | (df[column] > max_val)
            df.loc[mask, column] = np.nan
            df[column] = df[column].fillna(df[column].median())
    
    return df

def standardize_categorical_columns(df):
    """Standardize categorical columns"""
    categorical_columns = ['make', 'model', 'colour', 'fuel_type', 'test_type', 'test_result']
    
    for column in categorical_columns:
        if column in df.columns:
            # Convert to string and strip whitespace
            df[column] = df[column].astype(str).str.strip()
            # Convert to uppercase for consistency
            df[column] = df[column].str.upper()
            # Replace empty strings and 'nan' with N/A
            df[column] = df[column].replace(['', 'NAN', 'NONE', 'NULL'], 'N/A')
    
    return df

def load_cleaned_data(folder_path):
    """
    Load all cleaned CSV files in a folder into a single Pandas DataFrame.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")
    
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if not csv_files:
        raise ValueError(f"No CSV files found in the folder '{folder_path}'.")

    print(f"Found {len(csv_files)} cleaned CSV files.")
    
    dataframes = []
    
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        print(f"Loading file: {file_path}")
        
        try:
            df = pd.read_csv(file_path, quotechar='"', escapechar='\\')
            dataframes.append(df)
            print(f"Loaded file with shape: {df.shape}")
        except Exception as e:
            print(f"Error loading file {csv_file}: {e}")
    
    if not dataframes:
        raise ValueError("No data was successfully loaded from any file.")
    
    # Combine all dataframes
    combined_df = pd.concat(dataframes, ignore_index=True)
    print(f"Combined DataFrame shape: {combined_df.shape}")
    
    # Remove duplicates
    original_shape = combined_df.shape
    combined_df = combined_df.drop_duplicates()
    if combined_df.shape[0] < original_shape[0]:
        print(f"Removed {original_shape[0] - combined_df.shape[0]} duplicate rows")
    
    return combined_df

if __name__ == "__main__":
    # Folder containing the cleaned CSV files
    cleaned_data_folder = r"C:\Project\cleaned_data"
    
    try:
        # Load and validate the data
        mot_data = load_and_validate_data(cleaned_data_folder)
        
        # Print summary statistics
        print("\nSummary Statistics:")
        print(mot_data.describe())
        
        # Print information about data types and missing values
        print("\nDataset Info:")
        print(mot_data.info())
        
        # Print unique values in categorical columns
        categorical_columns = ['make', 'model', 'colour', 'fuel_type', 'test_type', 'test_result']
        print("\nUnique values in categorical columns:")
        for col in categorical_columns:
            if col in mot_data.columns:
                print(f"\n{col}: {mot_data[col].nunique()} unique values")
                print(mot_data[col].value_counts().head())
                
    except Exception as e:
        print(f"Error processing data: {e}")