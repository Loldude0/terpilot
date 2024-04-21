from tika import parser
import re
import json

possible_geneds = "FSAW|FSAR|FSMA|FSOC|FSPW|DSHS|DSHU|DSNS|DSNL|DSSP|DVCC|DVUP|SCIS"

raw = parser.from_file("unofficial transcript.pdf")

start_index = raw['content'].find("Historic Course Information")
end_index = raw['content'].find("Current Course Information")

query_string = raw['content'][start_index:end_index]
class_taken = re.findall(r"[A-Z]{4}[0-9]{3}[A-Z]?", query_string)

gened_query_string = raw['content'][:end_index]
geneds_fullfilled = re.findall(possible_geneds, gened_query_string)

print(class_taken)
print(geneds_fullfilled)

with open("geneds.json", "r") as f:
    contents = f.read()

res = []
courses = json.loads(contents)

for course in courses:
    if len(course["geneds"]) == 0:
        continue
    else:
        res.append((course["course_number"], course["geneds"]))

res.sort(key=lambda x: len(x[1]), reverse=True)
print(res)

suggestions = []
for course in res:
    if len(set(course[1])-set(geneds_fullfilled)) >= 2 and course[0] not in class_taken and course[0] not in [c[0] for c in suggestions]:
        suggestions.append(course)
        if len(suggestions) == 5:
            break

print(suggestions)

def get_suggestions():
    return suggestions