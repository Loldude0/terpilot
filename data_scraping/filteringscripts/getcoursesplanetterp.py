import os
import json

def get_unique_courses(directory, key):
    course_set = set()
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                print(f"Reading {filename}")
                data = json.load(f)
                if isinstance(data, list):  # For list type JSON files
                    for item in data:
                        course_set.add(item[key])
                else:  # For dict type JSON files
                    course_set.add(data[key])
    return list(course_set)

def write_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

grading_dir = '/home/atajne/terpilot/data_scraping/planetterp_data/course_grading'
info_dir = '/home/atajne/terpilot/data_scraping/planetterp_data/course_info'

grading_courses = get_unique_courses(grading_dir, 'course')
info_courses = get_unique_courses(info_dir, 'name')

grading_courses = list(dict.fromkeys(grading_courses))
info_courses = list(dict.fromkeys(info_courses))

grading_courses.sort()
info_courses.sort()

write_to_json({"grading_courses": grading_courses, "info_courses": info_courses}, 'unique_courses_planetterp.json')
