import os
import json

def combine_json_files(directory):
    combined_data = []

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)

            # Open each JSON file and load the data
            with open(filepath, 'r') as file:
                data = json.load(file)

            # Append the data to the combined_data list
            combined_data.append(data)

    # Write the combined data to a new JSON file
    with open('all_prof_info.json', 'w') as file:
        json.dump(combined_data, file, indent=4)

# Call the function with your directory
combine_json_files('/home/atajne/terpilot/data_scraping/planetterp_data/professor_info')
