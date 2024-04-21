import os
import json

def combine_json_files(directory, reference_file):
    with open(reference_file, 'r') as ref_file:
        reference_data = json.load(ref_file)

    combined_data = []

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                print(f'Processing {filename}')
                try:
                    data = json.load(f)
                except:
                    print(f'Error loading {filename}')
                    continue
                # Check if 'name' field is in reference_data
                if 'name' in data and data['name'] in reference_data:
                    combined_data.append(data)

    with open(os.path.join(directory, 'combined.json'), 'w') as outfile:
        json.dump(combined_data, outfile)

combine_json_files('/home/atajne/terpilot/data_scraping/planetterp_data/course_info', '/home/atajne/terpilot/data_scraping/final_data_json/courses_and_professors.json')
