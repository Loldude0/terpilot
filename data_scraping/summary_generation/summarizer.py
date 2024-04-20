import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
import ast
import json
import os
import glob
from collections import defaultdict
from time import sleep

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

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

model = genai.GenerativeModel("gemini-pro",safety_settings=safety_settings)

chat = model.start_chat()

def generate_summary(text):
    return text

#<------------------------SUMMARIZER------------------------>

def generate_summary_for_professor(professor_info):
    # Combine all reviews and their ratings for the professor
    all_reviews = " ".join([review["review"] for review in professor_info["reviews"]])
    all_ratings = [review["rating"] for review in professor_info["reviews"]]
    professor_summary = generate_summary(all_reviews)
    if not professor_summary:
        professor_summary = "No summary available due to lack of reviews"
    professor_rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0

    # Generate a summary for each course the professor has taught
    course_reviews = defaultdict(list)
    course_ratings = defaultdict(list)
    for review in professor_info["reviews"]:
        if review["course"]:
            course_reviews[review["course"]].append(review["review"])
            course_ratings[review["course"]].append(review["rating"])

    course_summaries = {}
    for course, reviews in course_reviews.items():
        combined_reviews = " ".join(reviews)
        course_summary = generate_summary(combined_reviews)

        if not course_summary:
            course_summary = "No summary available due to lack of reviews"
        course_summaries[course] = course_summary

    course_avg_ratings = {course: sum(ratings) / len(ratings) for course, ratings in course_ratings.items()}

    return {
        "name": professor_info["name"],
        "slug": professor_info["slug"],
        "courses": professor_info["courses"],
        "summary": professor_summary,
        "rating": professor_rating,
        "course_summaries": course_summaries,
        "course_ratings": course_avg_ratings,
    }

def generate_summaries(directory):
    summaries = []
    for filename in glob.glob(os.path.join(directory, "*.json")):
        with open(filename, "r") as file:
            print(f"Generating summary for {filename}")
            professor_info = json.load(file)
            summaries.append(generate_summary_for_professor(professor_info))

    # Write the summaries to a new JSON file
    with open("summaries.json", "w") as file:
        json.dump(summaries, file, indent=4)

generate_summaries("/home/atajne/terpilot/data_scraping/planetterp_data/professor_info")

#<------------------------SUMMARIZER------------------------>

def generate_summary_for_professor(professor_info):
    # Combine all reviews and their ratings for the professor
    all_reviews = " ".join([review["review"] for review in professor_info["reviews"]])
    all_ratings = [review["rating"] for review in professor_info["reviews"]]
    professor_summary = generate_summary(all_reviews)
    if not professor_summary:
        professor_summary = "No summary available due to lack of reviews"
    professor_rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0

    sleep(3)

    # Generate a summary for each course the professor has taught
    course_reviews = defaultdict(list)
    course_ratings = defaultdict(list)
    for review in professor_info["reviews"]:
        if review["course"]:
            course_reviews[review["course"]].append(review["review"])
            course_ratings[review["course"]].append(review["rating"])

    course_summaries = {}
    for course, reviews in course_reviews.items():
        combined_reviews = " ".join(reviews)
        course_summary = generate_summary(combined_reviews)
        sleep(2)
        if not course_summary:
            course_summary = "No summary available due to lack of reviews"
        course_summaries[course] = course_summary

    course_avg_ratings = {course: sum(ratings) / len(ratings) for course, ratings in course_ratings.items()}

    return {
        "name": professor_info["name"],
        "slug": professor_info["slug"],
        "courses": professor_info["courses"],
        "summary": professor_summary,
        "rating": professor_rating,
        "course_summaries": course_summaries,
        "course_ratings": course_avg_ratings,
    }

def generate_summaries(directory):
    summaries = []
    for filename in glob.glob(os.path.join(directory, "*.json")):
        with open(filename, "r") as file:
            print(f"Generating summary for {filename}")
            professor_info = json.load(file)
            summaries.append(generate_summary_for_professor(professor_info))
            sleep(5)

    # Write the summaries to a new JSON file
    with open("summaries.json", "w") as file:
        json.dump(summaries, file, indent=4)

generate_summaries("/home/atajne/terpilot/data_scraping/planetterp_data/professor_info")

