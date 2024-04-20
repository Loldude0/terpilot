import os
import json

def get_unique_professors(directory, key):
    professor_set = set()
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                print(f"Reading {filename}")
                data = json.load(f)
                if isinstance(data, list):  # For list type JSON files
                    for item in data:
                        professor_set.add(item[key])
                else:  # For dict type JSON files
                    professor_set.add(data[key])
    return list(professor_set)

def write_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

grading_dir = '/home/atajne/terpilot/data_scraping/planetterp_data/professor_grading'
info_dir = '/home/atajne/terpilot/data_scraping/planetterp_data/professor_info'

grading_professors = get_unique_professors(grading_dir, 'professor')
info_professors = get_unique_professors(info_dir, 'name')

write_to_json({"grading_professors": grading_professors, "info_professors": info_professors}, 'unique_professors_planetterp.json')