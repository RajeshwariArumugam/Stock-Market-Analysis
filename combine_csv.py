import os
import pandas as pd


input_folder = "PathToTheInputFile" #Replace it with the actual input file path
combined_data = pd.DataFrame()


for file_name in os.listdir(input_folder):
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)
        print(f"Processing file: {file_path}")  
        data = pd.read_csv(file_path)
        combined_data = pd.concat([combined_data, data], ignore_index=True)
        
output_file = "PathToTheOutputFile" #Replace it with the actual ouput file path 
combined_data.to_excel(output_file, index=False)
print(f"All data combined and saved to {output_file}")
