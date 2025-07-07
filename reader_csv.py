import pandas as pd
import os

COLUMN_NAMES = ['Timestamp', 'Description', 'Status', 'PID']

def remove_extra_spaces(data):
    # Remove leading and trailing spaces from all string columns in the DataFrame.
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = data[col].astype(str).str.strip()

    # Remove spaces within the 'Timestamp' and 'Status' columns and also convert 'Status' to uppercase.
    data['Timestamp'] = data['Timestamp'].str.replace(' ', '')
    data['Status'] = data['Status'].str.replace(' ', '').str.upper()
    return data

def read_and_parse_csv(input_path: str) -> pd.core.groupby.generic.DataFrameGroupBy:
    # This function reads a CSV file and parses it into a DataFrame, grouping by PID.

    if not os.path.exists(input_path):
        print(f"Error: File {input_path} doesn't exist.")
        return None
    
    try:
        data = pd.read_csv(input_path, header=None, names=COLUMN_NAMES)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    remove_extra_spaces(data)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%H:%M:%S')
    grouped = data.groupby("PID")
    return grouped
