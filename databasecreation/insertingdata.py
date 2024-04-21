import psycopg2
from psycopg2 import OperationalError
import os
import json
from dotenv import load_dotenv

load_dotenv()

connection_string = os.environ.get("CONNECTION_STRING")

print(connection_string)
conn = psycopg2.connect(dbname="postgres", user="postgres", password="terpilot", host="localhost", port="5432")

cur = conn.cursor()

#print the name of the database
cur.execute('SELECT current_database()')
db_name = cur.fetchone()[0]
print(f"Connected to the database '{db_name}'")

# Load the data from the JSON files
with open('/home/atajne/terpilot/data_scraping/finalthing/combined.json') as f:
    courses_data = json.load(f)

with open('/home/atajne/terpilot/data_scraping/final_data_json/combined_prof_info.json') as f:
    professors_data = json.load(f)

# Insert the data into the 'course', 'section', and 'professor' tables
for course in courses_data:
    print(course['course_number'])
    cur.execute("""
        INSERT INTO course (course_name, course_number, course_credits, course_grading, course_restriction, course_description, course_average_grade, course_grading_chart, course_prerequisites, course_corequisites)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING course_id
    """, (course['course_name'], course['course_number'], int(course.get('credits', 0)), course.get('grading_method', 'N/A'), course.get('restriction', 'N/A'), course.get('description', 'N/A'), float(course.get('average_gpa', 0)), course.get('grading', 'N/A'), course.get('prereq', 'N/A'), course.get('prereq', 'N/A')))
    course_id = cur.fetchone()[0]

    for section in course['sections']:
        cur.execute("""
            INSERT INTO section (section_name, course_name, course_id, professor_name, professor_rating, course_time, course_total_seats, course_open_seats, course_waitlist, course_summary, course_rating, course_location)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (section['section_id'], course['course_name'], course_id, section.get('professor', 'N/A'), float(section.get('rating', 0)), section.get('times', 'N/A'), int(section.get('total_seats', 0)), int(section.get('open_seats', 0)), int(section.get('waitlist', 0)), section.get('course_summary', 'N/A'), float(section.get('rating', 0)), section.get('locations', 'N/A')))

for professor in professors_data:
    average_rating = professor.get('average_rating')
    if average_rating is None:
        average_rating = 0.0
    cur.execute("""
        INSERT INTO professor (professor_name, professor_rating, professor_summary, professor_grading_chart)
        VALUES (%s, %s, %s, %s)
    """, (professor['name'], average_rating, professor.get('summary', 'N/A'), professor.get('grading', 'N/A')))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()