import psycopg2
from psycopg2 import OperationalError
import os
from dotenv import load_dotenv

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

def get_average_professor_rating_for_course(professor_name, course_name):
    cur.execute("""
        SELECT professor_rating
        FROM section
        WHERE professor_name = %s AND course_name = %s
    """, (professor_name, course_name))
    rating = cur.fetchone()
    if rating is None:
        return None
    return rating[0]