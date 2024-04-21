import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv
import re
from datetime import datetime

load_dotenv()

connection_string = os.environ.get("CONNECTION_STRING")
conn = psycopg2.connect(dbname="postgres", user="postgres", password="terpilot", host="localhost", port="5432")
cur = conn.cursor()

def get_average_professor_rating(professor_name):
    cur.execute("""
        SELECT professor_rating
        FROM professor
        WHERE professor_name = %s
    """, (professor_name))
    rating = cur.fetchone()
    if rating is None:
        return None
    return rating[0]

def get_professor_summary(professor_name):
    cur.execute("""
        SELECT professor_summary
        FROM professor
        WHERE professor_name = %s
    """, (professor_name,))
    summary = cur.fetchone()
    if summary is None:
        return None
    return summary[0]

def get_course_name_from_course_id(course_id):
    cur.execute("""
        SELECT course_name
        FROM course
        WHERE course_number = %s
    """, (course_id,))
    course_name = cur.fetchone()
    if course_name is None:
        return None
    return course_name[0]

def get_sections_time_from_course(course_name):
    cur.execute("""
        SELECT course_time, section_name
        FROM section
        WHERE course_name = %s
    """, (get_course_name_from_course_id(course_name),))
    time = cur.fetchall()
    return time

def parse_time_for_section(time):
    days = ['M', 'Tu', 'W', 'Th', 'F']
    schedule = [None]*5
    time_splits = time.split('|')
    for time_split in time_splits:
        day_time = re.findall(r'[A-Za-z]+|\d+:\d+[ap]m-\d+:\d+[ap]m', time_split.strip())
        for day in day_time[0]:
            for d in days:
                if day in d:
                    start_time, end_time = [datetime.strptime(t, "%I:%M%p") for t in day_time[1].split('-')]
                    duration = int((end_time - start_time).total_seconds() / 60)
                    schedule[days.index(d)] = start_time.strftime("%H%M") + str(duration).zfill(3)
    return schedule

def process_timetable(classes):
    timetable = {}
    for course_id in classes:
        sections_time = get_sections_time_from_course(course_id)
        for time, section_name in sections_time:
            if course_id not in timetable:
                timetable[course_id] = {}
            print(time)
            timetable[course_id][section_name] = parse_time_for_section(time)
    return timetable


print(process_timetable(["CMSC330", "CMSC351"]))