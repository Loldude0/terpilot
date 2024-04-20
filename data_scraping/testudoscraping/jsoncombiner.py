import json
import re

with open("list.html", "r") as file: #<-------------------->CHANGE<-------------------->
    courses_list = eval(file.read())

final_json = []
for course in courses_list:
    try:
        with open(course + ".json", "r") as file:
            data = json.load(file)
            final_json.append(data)
    except:
        print("Error in processing " + course + ".json")
        continue

with open("list.json", "w") as file: #<-------------------->CHANGE<-------------------->
    json.dump(final_json, file)