import json

# Load all the data from the json files
with open('/home/atajne/terpilot/data_scraping/course_section_data_final/courses_and_professors.json', 'r') as f:
    courses_and_professors = json.load(f)

with open('/home/atajne/terpilot/data_scraping/course_section_data_final/final_testudo_data.json', 'r') as f:
    final_testudo_data = json.load(f)

with open('/home/atajne/terpilot/data_scraping/course_section_data_final/avg_gpa_combined.json', 'r') as f:
    avg_gpa_combined = json.load(f)

with open('/home/atajne/terpilot/data_scraping/course_section_data_final/grading_statistics.json', 'r') as f:
    grading_statistics = json.load(f)

with open('/home/atajne/terpilot/data_scraping/course_section_data_final/summaries.json', 'r') as f:
    summaries = json.load(f)

# Combine the data
for course in final_testudo_data:
    course_number = course['course_number']
    print(f'Processing {course_number}')
    for gpa_data in avg_gpa_combined:
        if gpa_data['name'] == course_number:
            course['average_gpa'] = gpa_data['average_gpa']
            break
    for grading_data in grading_statistics:
        if grading_data['course'] == course_number:
            course['grading'] = grading_data['grading']
            break
    for summary_data in summaries:
        if course_number in summary_data['courses']:
            for section in course['sections']:
                if section['professor'] == summary_data['name']:
                    print("we found a match")

                    try:
                        section['course_summary'] = summary_data['course_summaries'][course_number]
                    except:
                        section['course_summary'] = 'no summary available'

                    try:
                        section['rating'] = summary_data['course_ratings'][course_number]
                    except:
                        section['rating'] = '0'

# Write the combined data to a new json file
with open('final_to_add.json', 'w') as f:
    json.dump(final_testudo_data, f, indent=4)
