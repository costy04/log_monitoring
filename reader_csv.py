import pandas as pd
import os

COLUMN_NAMES = ['Timestamp', 'Description', 'Status', 'PID']

def read_and_parse_csv(input_path):
# This function reads a CSV file and parses it into a DataFrame, grouping by PID.

    if not os.path.exists(input_path):
        print(f"Error: File {input_path} doesn't exist.")
        return None
    
    try:
        data = pd.read_csv(input_path, header=None, names=COLUMN_NAMES)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%H:%M:%S')
    grouped = data.groupby(["PID"])
    return grouped
