# Convert a CSV table to a JSON table in a new file

import csv
import json


csv_file_path = 'r1.csv'  # Replace with the path to your CSV file
selected_column = 'Statement'  # Replace with the name of the column you want to keep
output_json_file = 'train_phase0.json'  # Replace with the desired output JSON file path

csvfile = open(csv_file_path, 'r', newline='', encoding='utf-8')  # Specify encoding if needed
jsonfile = open(output_json_file, 'w')

# Use DictReader without specifying fieldnames
reader = csv.DictReader(csvfile)

for row in filter(lambda row: row[selected_column].strip(), reader):
    # Create a dictionary with only the selected column
    selected_data = {
        'text': row[selected_column],
        'label': 1
    }
    
    # Write the selected data to the JSON file
    json.dump(selected_data, jsonfile)
    jsonfile.write('\n')

csvfile.close()
jsonfile.close()

print(f'The result has been saved to {output_json_file}')
