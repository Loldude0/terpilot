import json
import requests
import os

# Load the list of courses
with open('/home/aryantajne/terpilot/unique_courses.json', 'r') as f:
    courses = json.load(f)

# For each course in the list
for course in courses:
    # Call the API
    response = requests.get(
        "https://planetterp.com/api/v1/course",
        params={
            "name": course,
            "reviews": "true"
        }
    )

    # If the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        print(f"Fetched data for {course}")
        data = response.json()

        # Write the data to a JSON file
        with open(f'/home/aryantajne/terpilot/{course.replace(" ", "_")}.json', 'w') as f:
            json.dump(data, f)
    else:
        print(f"Failed to fetch data for {course}")
