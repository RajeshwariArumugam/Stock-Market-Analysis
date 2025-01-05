import os
import yaml
import pandas as pd

# Define the root directory containing the month-wise folders
root_dir = r"D:\pro_2"
output_dir = r"D:\pro_2\csv_files"
os.makedirs(output_dir, exist_ok=True)

# Dictionary to store data by Ticker (symbol)
data_by_symbol = {}

# Iterate through the month-wise folders
for month_folder in os.listdir(root_dir):
    month_path = os.path.join(root_dir, month_folder)
    if os.path.isdir(month_path):
        # Iterate through YAML files in each month's folder
        for yaml_file in os.listdir(month_path):
            if yaml_file.endswith(".yaml"):
                file_path = os.path.join(month_path, yaml_file)
                
                # Load the YAML file
                with open(file_path, 'r') as file:
                    try:
                        yaml_data = yaml.safe_load(file)
                        
                        # Check if the YAML data is a list
                        if isinstance(yaml_data, list):
                            for entry in yaml_data:
                                ticker = entry.get('Ticker')
                                if ticker:
                                    if ticker not in data_by_symbol:
                                        data_by_symbol[ticker] = []
                                    data_by_symbol[ticker].append(entry)
                        elif isinstance(yaml_data, dict):
                            ticker = yaml_data.get('Ticker')
                            if ticker:
                                if ticker not in data_by_symbol:
                                    data_by_symbol[ticker] = []
                                data_by_symbol[ticker].append(yaml_data)
                    except yaml.YAMLError as e:
                        print(f"Error reading {file_path}: {e}")

# Convert data for each Ticker into a CSV file
for ticker, records in data_by_symbol.items():
    df = pd.DataFrame(records)
    output_file = os.path.join(output_dir, f"{ticker}.csv")
    df.to_csv(output_file, index=False)
    print(f"CSV created for {ticker}: {output_file}")
