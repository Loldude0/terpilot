import json
import re

list = [
    "cmsc",
    "dshs",
    "dshu",
    "dsnl",
    "dsns",
    "dssp",
    "dvcc",
    "dvup",
    "fsaw",
    "fsma",
    "fsoc",
    "fspw",
    "scis"
]
courses_list = []
def doit(name):
    with open(r"/home/atajne/terpilot/data_scraping/raw/" + name + "/" + name + ".html", "r") as file: #<-------------------->CHANGE<-------------------->
        courses_listy = eval(file.read())
        courses_list.extend(courses_listy)

for name in list:
    doit(name)

print(courses_list)

final_json = []
for course in courses_list:
    print(course)
    try:
        with open(course + ".json", "r") as file:
            data = json.load(file)
            final_json.append(data)
    except:
        print("Error in processing " + course + ".json")
        continue

with open("listo.json", "w") as file: #<-------------------->CHANGE<-------------------->
    print(final_json)
    json.dump(final_json, file)