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
    class_lst = tmp_time_data
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
    context_manager.swap_system_message(f"""
        [SYSTEM PRPMPT]
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
        [SYSTEM PRPMPT]
        You are a summary generator that generates a summary of a given text.
        You should summarize the text in a short, consise manner.
    """)
    summary_context_manager.add_context("model","Sure, I can help with summarizing the text.")
    chat = summary_model.start_chat(history=summary_context_manager.get_context())
    response = chat.send_message(input_text).text

    return response, response, "text-data"

def generate_professor_summary(professor_name, context_manager):
    professor_name = "Maksym Morawski"
    average_rating = 4.5
    summary = generate_summary("", context_manager)
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

if __name__ == "__main__":
    print(generate_schedule(["CMSC330", "CMSC351", "ENGL101"], None))