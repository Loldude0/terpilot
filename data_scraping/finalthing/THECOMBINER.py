import json

# Load the data from both files
with open('/home/atajne/terpilot/data_scraping/finalthing/final_to_add2.json', 'r') as file1, \
     open('/home/atajne/terpilot/data_scraping/finalthing/list.json', 'r') as file2:
    data1 = json.load(file1)
    data2 = json.load(file2)

# Convert the second file's data into a dictionary for easy lookup
data2_dict = {(item['course_number'], section['section_id']): section['locations'] 
              for item in data2 if 'sections' in item for section in item['sections']}

# Add the locations from the second file to the first file's data
for item in data1:
    for section in item['sections']:
        key = (item['course_number'], section['section_id'])
        if key in data2_dict:
            section['locations'] = data2_dict[key]

# Write the combined data to a new file
with open('/home/atajne/terpilot/data_scraping/finalthing/combined.json', 'w') as outfile:
    json.dump(data1, outfile, indent=4)