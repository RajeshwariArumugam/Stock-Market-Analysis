import os
import yaml
import pandas as pd


root_dir = r"PathOfInputFile"
output_dir = r"PathOfOutputFile"
os.makedirs(output_dir, exist_ok=True)

data_by_symbol = {}


for month_folder in os.listdir(root_dir):
    month_path = os.path.join(root_dir, month_folder)
    if os.path.isdir(month_path):
        for yaml_file in os.listdir(month_path):
            if yaml_file.endswith(".yaml"):
                file_path = os.path.join(month_path, yaml_file)
                with open(file_path, 'r') as file:
                    try:
                        yaml_data = yaml.safe_load(file)
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
for ticker, records in data_by_symbol.items():
    df = pd.DataFrame(records)
    output_file = os.path.join(output_dir, f"{ticker}.csv")
    df.to_csv(output_file, index=False)
    print(f"CSV created for {ticker}: {output_file}")
