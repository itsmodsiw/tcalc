import json
from PyQt6.QtWidgets import QApplication, QFileDialog

def convert_to_json(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as f:
        ids = f.read().splitlines()

    # Convert IDs to JSON format
    json_data = []
    for id in ids:
        json_data.append({'id': id})

    # Write the JSON data to the output file
    with open(output_file, 'w') as f:
        json.dump(json_data, f, indent=4)

# Create a PyQt6 application
app = QApplication([])

# Prompt the user for the input file location
input_file, _ = QFileDialog.getOpenFileName(None, 'Select Input File')

# Prompt the user for the output file path
output_file, _ = QFileDialog.getSaveFileName(None, 'Select Output File', '', 'JSON Files (*.json)')

# Convert to JSON format
if input_file and output_file:
    convert_to_json(input_file, output_file)
    print('Conversion completed successfully.')

# Exit the application
app.exit()
