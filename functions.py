from graph import DirectionalGraph, CoursePrerequisiteGraph
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gemini_context_manager import GeminiContextManager
import re
from functions import *
import ast
import json
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv
from parse_usr_data import get_suggestions

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="terpilot",
    host="localhost",
    port="5432",
)
cur = conn.cursor()

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-pro", safety_settings=safety_settings)
summary_model = genai.GenerativeModel(
    "gemini-1.5-pro-latest", safety_settings=safety_settings
)

tmp_time_data = {
    "CMSC330": {
        "0101": ["1130050", None, "1130050", None, None],
        "0102": ["1130050", None, "0930050", None, None],
    },
    "CMSC351": {
        "0101": ["0830050", None, "1330050", None, None],
        "0102": ["1130050", None, " 0930050", None, None],
    },
    "ENGL101": {
        "0101": [None, "0800075", None, None, "1600050"],
        "0102": ["1130050", None, "0930050", None, None],
    },
}


def check_time_slot(time_table, day, start_time, duration):
    start_hour = int(start_time[:2])
    start_minute = int(start_time[2:])
    duration = int(int(duration) / 10)
    return (
        time_table[day * 24 * 6 + start_hour * 6 + int(start_minute / 10)] == False
    ) & (
        time_table[day * 24 * 6 + start_hour * 6 + int(start_minute / 10) + duration]
        == False
    )


def generate_schedule_aux(class_lst, time_table, idx, lst, res):
    class_names = list(class_lst.keys())  # ["CMSC330", "CMSC351", "ENGL101]
    # print(class_names)
    sections = class_lst[
        class_names[idx]
    ]  # {"0101":["1130050", None, "1130050", None, None], "0102": ["1130050", None, "0930050", None, None]}
    section_names = sections.keys()
    for section_name in section_names:
        time_lst = sections[section_name]
        cpy_time_table = time_table.copy()
        for i in range(5):  # for each day
            time = time_lst[i]
            if time is not None:
                start_time = time[:4]
                duration = time[4:]
                if not check_time_slot(time_table, i, start_time, duration):
                    break
                for j in range(int(int(duration) / 10)):
                    cpy_time_table[
                        i * 24 * 6
                        + int(start_time[:2]) * 6
                        + int(int(start_time[2:4]) / 10)
                        + j
                    ] = True
        else:
            lst_cpy = lst.copy()
            lst_cpy.append(class_names[idx] + "-" + section_name)
            if idx == len(class_names) - 1:
                res.append(lst_cpy)
                break
            generate_schedule_aux(class_lst, cpy_time_table, idx + 1, lst_cpy, res)

    return


def generate_schedule(lst, context_manager):
    class_lst = process_timetable(lst)
    res = []
    time_table = [False] * 5 * 24 * 6
    generate_schedule_aux(class_lst, time_table, 0, [], res)
    print(res)
    res = convert_to_schedule(res)
    res = [
        {"start": "Monday", "start_time": "09:00", "end_time": "10:00", "text": "Math"},
        {
            "start": "Monday",
            "start_time": "10:00",
            "end_time": "11:00",
            "text": "English",
        },
        {
            "start": "Tuesday",
            "start_time": "09:00",
            "end_time": "10:00",
            "text": "Science",
        },
        {
            "start": "Tuesday",
            "start_time": "10:00",
            "end_time": "11:00",
            "text": "History",
        },
    ]
    message = "Here is a schedule for the classes: {res}"
    return res, message, "schedule-data"


def verify_courses(graph, course_lst):
    for course in course_lst:
        if not graph.is_satisfied(course):
            course_lst.remove(course)
    return


def general_chat(input_text, context_manager):
    context_manager.swap_system_message(
        f"""s
        [SYSTEM PROMPT]
        You are a friendly copilot that helps students in the University of Maryland perform various tasks regarding our ELMS.
        You should refer to yourself as "Terpilot" when talking to the user.
        Always respond with concise and short messages.
        
    """,
        "Hi, this is your friendly copilot, Terpilot. How can I help you today?",
    )
    chat = model.start_chat(history=context_manager.get_context())
    response = chat.send_message(input_text).text

    return response, response, "text-data"


def generate_summary(input_text, context_manager):
    summary_context_manager = GeminiContextManager()
    summary_context_manager.add_context(
        "user"
        f"""
        [SYSTEM PROMPT]
        You are a summary generator that generates a summary of a given text.
        You should summarize the text in a short, consise manner within 128 words.
    """
    )
    summary_context_manager.add_context(
        "model", "Sure, I can help with summarizing the text."
    )
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
    return {"name": "251 North", "lng": -76.9496090325357, "lat": 38.99274005}


def get_map_data(class_lst, context_manager):
    # locations_lst = search_location(class_lst)
    location_lst = [
        {"name": "251 North", "lng": -76.9496090325357, "lat": 38.99274005},
        {"name": "94th Aero Squadron", "lng": -76.9210122711411, "lat": 38.9781702},
    ]
    return (
        location_lst,
        "Here are the location of the classes: {location_lst}",
        "geo-data",
    )


def get_average_professor_rating(professor_name):
    cur.execute(
        """
        SELECT professor_rating
        FROM professor
        WHERE professor_name = %s
    """,
        (professor_name),
    )
    rating = cur.fetchone()
    if rating is None:
        return None
    return rating[0]


def get_professor_summary(professor_name):
    cur.execute(
        """
        SELECT professor_summary
        FROM professor
        WHERE professor_name = %s
    """,
        (professor_name,),
    )
    summary = cur.fetchone()
    if summary is None:
        return None
    return summary[0]


def get_course_name_from_course_id(course_id):
    cur.execute(
        """
        SELECT course_name
        FROM course
        WHERE course_number = %s
    """,
        (course_id,),
    )
    course_name = cur.fetchone()
    if course_name is None:
        return None
    return course_name[0]


def get_sections_time_from_course(course_name):
    cur.execute(
        """
        SELECT course_time, section_name
        FROM section
        WHERE course_name = %s
    """,
        (get_course_name_from_course_id(course_name),),
    )
    time = cur.fetchall()
    return time


def parse_time_for_section(time):
    days = ["M", "Tu", "W", "Th", "F"]
    schedule = [None] * 5
    time_splits = time.split("|")
    for time_split in time_splits:
        day_time = re.findall(
            r"[A-Za-z]+|\d+:\d+[ap]m-\d+:\d+[ap]m", time_split.strip()
        )
        for day in day_time[0]:
            for d in days:
                if day in d:
                    start_time, end_time = [
                        datetime.strptime(t, "%I:%M%p") for t in day_time[1].split("-")
                    ]
                    duration = int((end_time - start_time).total_seconds() / 60)
                    schedule[days.index(d)] = start_time.strftime("%H%M") + str(
                        duration
                    ).zfill(3)
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


def get_course_information(course_id):
    cur.execute(
        """
        SELECT course_name, course_description, course_credits, course_prerequisites, course_corequisites, course_grading, course_restriction, course_average_grade
        FROM course
        WHERE course_number = %s
    """,
        (course_id,),
    )
    course_info = cur.fetchone()
    if course_info is None:
        return None
    return course_info


def get_sections_for_course(course_id):
    cur.execute(
        """
        SELECT section_name, professor_name, professor_rating, course_time, course_total_seats, course_open_seats, course_waitlist, course_rating, course_location
        FROM section
        WHERE course_name = %s
    """,
        (get_course_name_from_course_id(course_id),),
    )
    sections = cur.fetchall()
    return sections


def get_section_location(section_name):
    cur.execute(
        """
        SELECT course_location
        FROM section
        WHERE section_name = %s
    """,
        (section_name,),
    )
    location = cur.fetchone()
    if location is None:
        return None
    return location[0]


hardcoded_lat_long_bldg = {
    "AJC": "38.99173753565603, -76.93765960691319",
    "ANA": "38.98588847314928, -76.94675983309673",
    "ANS": "38.99163676132008, -76.9399988435181",
    "ARC": "38.984444041128114, -76.94775200755643",
    "ARM": "38.98607880650188, -76.93837126932418",
    "ASY": "38.98517079687454, -76.94744106554863",
    "ATL": "38.99085370276552, -76.9416782293068",
    "AVW": "38.990747419308065, -76.93635134691868",
    "BLD2": "38.984258651235834, -76.9334910512356",
    "BLD4": "38.984258651235834, -76.9334910512356",
    "BPS": "38.98880916200182, -76.94244944011893",
    "BRB": "38.98914208194301, -76.94316086266753",
    "CCC": "38.99196242883344, -76.94307693012547",
    "CHE": "38.990482555312624, -76.93925739903358",
    "CHI": "38.98529972325033, -76.94456775082956",
    "CHM": "38.989342284862985, -76.94002668992984",
    "CSI": "38.98994601902395, -76.93621518384744",
    "DOR": "38.98667355351174, -76.94626715986199",
    "EDU": "38.986722246256946, -76.94723276917877",
    "EGR": "38.98889329768932, -76.93809736318984",
    "ESJ": "38.987141994601515, -76.94233664841482",
    "HBK": "38.98818262423956, -76.94195884184998",
    "HJP": "38.98708034223007, -76.94315608321874",
    "IRB": "38.98942936466464, -76.93637776212825",
    "JMP": "38.99077335154235, -76.93995933826154",
    "JMZ": "38.98680206509735, -76.94454037694105",
    "JUL": "38.99088882500949, -76.94362146322534",
    "KEB": "38.99084572773106, -76.93785749747822",
    "KEY": "38.98519547548969, -76.94304265330857",
    "KNI": "38.986915409260625, -76.94841606503057",
    "LEF": "38.983867833770034, -76.94397789193872",
    "MCB": "38.988069161989095, -76.94350408164941",
    "MMH": "38.985199473488784, -76.94075730606896",
    "MTH": "38.98828258782535, -76.93913673995033",
    "PAC": "38.990887369058754, -76.9505739217319",
    "PBR": "38.98471171928251, -76.93330259861202",
    "PFR": "38.98471171928251, -76.93330259861202",
    "PHY": "38.98814441910953, -76.9401748622026",
    "PLS": "38.988830604212765, -76.94093522189544",
    "QAN": "38.98533865567339, -76.9462051027167",
    "SHM": "38.98393913552208, -76.94265226175052",
    "SKN": "38.984740830555964, -76.94190449342847",
    "SPH": "38.993369868826555, -76.94323265710165",
    "SQH": "38.98212065580941, -76.94380202321544",
    "SYM": "38.98711064137635, -76.94060951518915",
    "TBA": "38.99031360603025, -76.9443496080395",
    "TLF": "38.98475944529583, -76.94311161850442",
    "TMH": "38.98505000173372, -76.93865596768457",
    "TWS": "38.98600431367601, -76.947707845584",
    "TYD": "38.9850558261271, -76.9440536432023",
    "VMH": "38.98311830054672, -76.94693288977115",
    "WDS": "38.98525385694827, -76.94185378821577",
    "YDH": "38.984258651235834, -76.9334910512356",
}


def get_lat_long_bldg(bldg):
    return hardcoded_lat_long_bldg[bldg]


def get_course_location(course_id):
    sections = get_sections_for_course(course_id)
    location = []
    for section in sections:
        location.append(get_section_location(section[0]))

    latlonglist = []
    for loc in location:
        locs = loc.split(" | ")
        print(locs)
        for l in locs:
            latlonglist.append(get_lat_long_bldg(l.split(" ")[0].strip()))

    return list(set(latlonglist))

def make_suggestions(context_manager):
    suggestions = get_suggestions()
    response_string = """
    Based on your unofficial transcript, here are some courses that you should take:
    """ + "\n".join([suggestion[0] + ': fullfills ' + ','.join(suggestion[1]) for suggestion in suggestions])
    print(suggestions)
    return suggestions, "Here are some course suggestions: {suggestions}", "text-data"

if __name__ == "__main__":
    print(generate_schedule(["CMSC330", "CMSC351", "ENGL101"], None))
