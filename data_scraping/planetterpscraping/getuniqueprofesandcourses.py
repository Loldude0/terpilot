import re
import os
import json

FILE_DIR = r"/home/aryantajne/terpilot/data_file"

unique_profs = []
unique_courses = []

#go through every file in the directory, the names are different and the format is in json
for file in os.listdir(FILE_DIR):
    with open(os.path.join(FILE_DIR, file), 'r') as f:
        print(file)
        data = json.load(f)
        for course in data:
            if course['course_number'] not in unique_courses:
                unique_courses.append(course['course_number'])
                print(course['course_number'])
            try:
                for sections in course['sections']:
                    if sections['professor'] not in unique_profs:
                        unique_profs.append(sections['professor'])
            except:
                pass

#write to file
with open('unique_profs.json', 'w') as f:
    json.dump(unique_profs, f)

with open('unique_courses.json', 'w') as f:
    json.dump(unique_courses, f)