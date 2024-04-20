import json

def read_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def write_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_courses_and_professors(data):
    course_professor_dict = {}
    for item in data:
        course = item['course_number']
        professors = [section['professor'] for section in item['sections']]
        course_professor_dict[course] = list(set(professors))  # Remove duplicates
    return course_professor_dict

filename = r'/home/atajne/terpilot/data_scraping/final_data_json/final_testudo_data.json'
data = read_from_json(filename)

course_professor_dict = get_courses_and_professors(data)

write_to_json(course_professor_dict, 'courses_and_professors.json')