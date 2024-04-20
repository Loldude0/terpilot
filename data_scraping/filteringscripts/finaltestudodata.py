import os
import json

def read_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def write_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def process_data(directory, courses, professors):
    processed = 0
    removed = 0
    removed_section = 0
    written = 0
    removed_courses = []
    removed_courses_due_to_missing_section = []
    final_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                print(f"Processing {filename}")
                data = json.load(f)
                for item in data:
                    processed += 1
                    print(f"    Processing {item['course_number']}")
                    if item['course_number'] not in courses:
                        removed_courses.append(item['course_number'])
                        removed += 1
                        continue
                    try:
                        sections = item['sections']
                    except:
                        removed_courses_due_to_missing_section.append(item['course_number'])
                        removed += 1
                        continue
                    for section in sections:
                        if section['professor'] not in professors:
                            sections.remove(section)
                            removed_section += 1
                    if sections:
                        item['sections'] = sections
                        final_data.append(item)
                        written += 1
                    else:
                        removed_courses_due_to_missing_section.append(item['course_number'])
                        removed_section += 1
    return final_data, processed, removed, removed_section, written, removed_courses, removed_courses_due_to_missing_section

courses_file = '/home/atajne/terpilot/data_scraping/intermediatedata/unique_courses_planetterp.json'
professors_file = '/home/atajne/terpilot/data_scraping/intermediatedata/unique_professors_planetterp.json'
data_dir = '/home/atajne/terpilot/data_scraping/testudo_data'

courses_data = read_from_json(courses_file)
professors_data = read_from_json(professors_file)

final_courses = courses_data['final_list']
final_professors = professors_data['final_list']

final_data, processed, removed, removed_section, written, a, b = process_data(data_dir, final_courses, final_professors)

print(f"Processed: {processed}")
print(f"Removed: {removed}")
print(f"Removed section: {removed_section}")
print(f"Written: {written}")
print(f"Removed courses: {a}")
print(f"Removed courses due to missing sections: {b}")
print(f"professors: {final_professors}")

write_to_json(final_data, 'final_testudo_data.json')