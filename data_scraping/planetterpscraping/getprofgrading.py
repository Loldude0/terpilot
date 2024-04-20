import json
import requests
import os

# Load the list of professors
with open('/home/aryantajne/terpilot/unique_profs.json', 'r') as f:
    professors = json.load(f)

# For each professor in the list
for professor in professors:
    # Call the API
    response = requests.get(
        "https://planetterp.com/api/v1/grades",
        params={
            "professor": professor
        }
    )

    # If the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        print(f"Fetched data for {professor}")
        data = response.json()

        # Write the data to a JSON file
        with open(f'/home/aryantajne/terpilot/{professor.replace(" ", "_")}_grades.json', 'w') as f:
            json.dump(data, f)
    else:
        print(f"Failed to fetch data for {professor}")
