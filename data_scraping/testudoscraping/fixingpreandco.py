import json
import re

def process_text(text):
    if len(text) == 7:
        return text
    else:
        parts = re.split(';', text)
        processed_parts = []
        for part in parts:
            processed_part = part[-8:].strip()
            if re.match('^[A-Z0-9]*$', processed_part):
                processed_parts.append(processed_part)
        if 'and' in text:
            # take 9 characters before and after the and and then strip them then add to the list
            before_and = text.split('and')[0][-9:].strip()
            after_and = text.split('and')[1][:9].strip()
            if re.match('^[A-Z0-9]*$', before_and):
                processed_parts.append(before_and)
            if re.match('^[A-Z0-9]*$', after_and):
                processed_parts.append(after_and)
            #remove duplicates
            processed_parts = list(set(processed_parts))
        return ', '.join(processed_parts)

with open("list.html", "r") as file: #<-------------------->CHANGE<-------------------->
    courses_list = eval(file.read())

for course in courses_list:
    try:
        with open(course + ".json", "r") as file:
            print("Processing " + course)
            data = json.load(file)
            if 'prereq' in data:
                data['prereq'] = process_text(data['prereq'])
            if 'coreq' in data:
                data['coreq'] = process_text(data['coreq'])
        with open(course + ".json", "w") as file:
            json.dump(data, file)
    except:
        print("Error in processing " + course + ".json")
        continue