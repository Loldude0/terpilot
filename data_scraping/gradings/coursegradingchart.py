import os
import json
from collections import defaultdict

# Define the directory containing the JSON files
directory = "/home/atajne/terpilot/data_scraping/planetterp_data/course_grading"

# Define the grades we are interested in
grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F", "W", "Other"]

# Initialize a list to hold the results
results = []

with open("/home/atajne/terpilot/data_scraping/intermediatedata/unique_courses_planetterp.json", 'r') as f:
    final_list = json.load(f)["final_list"]

# Loop over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename), 'r') as f:
            print(f"Processing {filename}")
            data = json.load(f)
            try:
                if data[0]["course"] not in final_list:
                    continue
            except:
                continue
        # Initialize a dictionary to hold the grading statistics for this course
        course_stats = defaultdict(lambda: defaultdict(int))

        # Loop over each record in the data
        for record in data:
            # Loop over each grade
            for grade in grades:
                # Add the count for this grade to the total for the professor and the overall total
                course_stats[record["professor"]][grade] += record[grade]
                course_stats["OVERALL"][grade] += record[grade]

        # Prepare the result for this course
        result = {"course": data[0]["course"]}

        # Convert the grading statistics to text format
        grading = []
        for professor, stats in course_stats.items():
            grading.append(f"{professor} - " + ", ".join(f"{grade}:{count}" for grade, count in stats.items()))
        result["grading"] = "; ".join(grading)

        # Add the result for this course to the list of results
        results.append(result)

# Write the results to a new JSON file
with open("grading_statistics.json", 'w') as f:
    json.dump(results, f, indent=4)