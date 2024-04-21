import os
import json
from collections import defaultdict

# Define the directory containing the JSON files
directory = "/home/atajne/terpilot/data_scraping/planetterp_data/professor_grading"

# Load the final list of professors
with open("/home/atajne/terpilot/data_scraping/intermediatedata/unique_professors_planetterp.json", 'r') as f:
    final_list = json.load(f)["final_list"]

# Define the grades we are interested in
grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F", "W", "Other"]

# Initialize a list to hold the results
results = []

# Loop over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename), 'r') as f:
            data = json.load(f)

        # Skip this file if the professor is not in the final list
        try:
            if data[0]["professor"] not in final_list:
                continue
        except:
            continue
        
        # Initialize a dictionary to hold the grading statistics for this professor
        professor_stats = defaultdict(lambda: defaultdict(int))

        # Loop over each record in the data
        for record in data:
            # Loop over each grade
            for grade in grades:
                # Add the count for this grade to the total for the course and the overall total
                professor_stats[record["course"]][grade] += record[grade]
                professor_stats["OVERALL"][grade] += record[grade]

        # Prepare the result for this professor
        result = {"professor": data[0]["professor"]}

        # Convert the grading statistics to text format
        grading = []
        for course, stats in professor_stats.items():
            grading.append(f"{course} - " + ", ".join(f"{grade}:{count}" for grade, count in stats.items()))
        result["grading"] = "; ".join(grading)

        # Add the result for this professor to the list of results
        results.append(result)

# Write the results to a new JSON file
with open("professor_grading_statistics.json", 'w') as f:
    json.dump(results, f, indent=4)