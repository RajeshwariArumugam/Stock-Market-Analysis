import os
import pandas as pd

# Define the input folder containing the CSV files
input_folder = "PathToTheInputFile" #Replace it with the actual input file path

# Initialize an empty DataFrame to combine all data
combined_data = pd.DataFrame()

# Loop through all files in the folder
for file_name in os.listdir(input_folder):
    # Check if the file is a CSV file
    if file_name.endswith(".csv"):
        file_path = os.path.join(input_folder, file_name)
        print(f"Processing file: {file_path}")  # Debug: Print the file being processed

        # Read the CSV file
        data = pd.read_csv(file_path)

        # Append the data to the combined DataFrame
        combined_data = pd.concat([combined_data, data], ignore_index=True)

# Define the output file path
output_file = "PathToTheOutputFile" #Replace it with the actual output file path where we need to store

# Save the combined DataFrame to an Excel file
combined_data.to_excel(output_file, index=False)
print(f"All data combined and saved to {output_file}")
