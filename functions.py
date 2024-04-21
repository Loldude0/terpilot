from graph import DirectionalGraph, CoursePrerequisiteGraph
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gemini_context_manager import GeminiContextManager
import re
from functions import *
import ast
import json

import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv

conn = psycopg2.connect(dbname="postgres", user="postgres", password="terpilot", host="localhost", port="5432")
cur = conn.cursor()

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro",safety_settings=safety_settings)
summary_model = genai.GenerativeModel("gemini-1.5-pro-latest",safety_settings=safety_settings)

tmp_time_data = {
    "CMSC330": {"0101":["1130050", None, "1130050", None, None], "0102": ["1130050", None, "0930050", None, None]},
    "CMSC351": {"0101":["0830050", None, "1330050", None, None], "0102": ["1130050", None," 0930050", None, None]},
    "ENGL101": {"0101":[None, "0800075", None, None, "1600050"], "0102": ["1130050", None, "0930050", None, None]}
}

def check_time_slot(time_table,day,start_time,duration):
    start_hour = int(start_time[:2])
    start_minute = int(start_time[2:])
    duration = int(int(duration)/10)
    return (time_table[day*24*6 + start_hour*6 + int(start_minute/10)] == False) & (time_table[day*24*6 + start_hour*6 + int(start_minute/10) + duration] == False)

def generate_schedule_aux(class_lst, time_table, idx, lst, res):
    class_names = list(class_lst.keys()) # ["CMSC330", "CMSC351", "ENGL101]
    #print(class_names)
    sections = class_lst[class_names[idx]] # {"0101":["1130050", None, "1130050", None, None], "0102": ["1130050", None, "0930050", None, None]}
    section_names = sections.keys()
    for section_name in section_names:
        time_lst = sections[section_name]
        cpy_time_table = time_table.copy()
        for i in range(5): # for each day
            time = time_lst[i]
            if time is not None:
                start_time = time[:4]
                duration = time[4:]
                if not check_time_slot(time_table, i, start_time, duration):
                    break
                for j in range(int(int(duration)/10)):
                    cpy_time_table[i*24*6 + int(start_time[:2])*6 + int(int(start_time[2:4])/10) + j] = True
        else:
            lst_cpy = lst.copy()
            lst_cpy.append(class_names[idx]+"-"+section_name)
            if idx == len(class_names) - 1:
                res.append(lst_cpy)
                break
            generate_schedule_aux(class_lst, cpy_time_table, idx+1, lst_cpy, res)
    
    return
                    

def generate_schedule(lst, context_manager):
    class_lst = process_timetable(lst)
    res = []
    time_table = [False] * 5 * 24 * 6
    generate_schedule_aux(class_lst, time_table, 0, [], res)
    print(res)
    res_dict = {
        f"Choice{i+1}": [" Section ".join(class_item.split("-")) for class_item in res[i]] for i in range(len(res))
    }
    message = f"Here are the possible schedules: {res_dict}"
    return res, message, "text-data"

def verify_courses(graph, course_lst):
    for course in course_lst:
        if not graph.is_satisfied(course):
            course_lst.remove(course)      
    return

def general_chat(input_text, context_manager):
    context_manager.swap_system_message(f"""s
        [SYSTEM PROMPT]
        You are a friendly copilot that helps students in the University of Maryland perform various tasks regarding our ELMS.
        You should refer to yourself as "Terpilot" when talking to the user.
        Always respond with concise and short messages.
        
    """, "Hi, this is your friendly copilot, Terpilot. How can I help you today?")
    chat = model.start_chat(history=context_manager.get_context())
    response = chat.send_message(input_text).text
    
    return response, response, "text-data"

def generate_summary(input_text, context_manager):
    summary_context_manager = GeminiContextManager()
    summary_context_manager.add_context("user"f"""
        [SYSTEM PROMPT]
        You are a summary generator that generates a summary of a given text.
        You should summarize the text in a short, consise manner within 128 words.
    """)
    summary_context_manager.add_context("model","Sure, I can help with summarizing the text.")
    chat = summary_model.start_chat(history=summary_context_manager.get_context())
    response = chat.send_message(input_text).text

    return response, response, "text-data"

def generate_professor_summary(professor_name, context_manager):
    fetched_summary = get_professor_summary(professor_name)
    summary = ""
    if fetched_summary is None:
        summary = "Unfortunately, there are not enough reviews for me to analyze and generate a summary."
    else:
        summary = generate_summary(fetched_summary, context_manager)

    average_rating = get_average_professor_rating(professor_name)
    full_summary = f"""
                Here is a summary of Professor {professor_name}.
                Average Rating: {average_rating}
                {summary}"""
    return full_summary, full_summary, "text-data"

def search_location(class_name, section):
    return {"name":"251 North", "lng": -76.9496090325357, "lat": 38.99274005}

def get_map_data(class_lst, context_manager):
    #locations_lst = search_location(class_lst)
    location_lst = [{"name":"251 North", "lng": -76.9496090325357, "lat": 38.99274005}, {"name": "94th Aero Squadron", "lng": -76.9210122711411, "lat": 38.9781702}]
    return location_lst, "Here are the location of the classes: {location_lst}", "geo-data"

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

if __name__ == "__main__":
    print(generate_schedule(["CMSC330", "CMSC351", "ENGL101"], None))