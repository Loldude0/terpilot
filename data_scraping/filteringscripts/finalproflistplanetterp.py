import json

def read_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def write_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_intersection_and_difference(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    intersection = set1 & set2
    difference1 = set1 - set2
    difference2 = set2 - set1
    return list(intersection), list(difference1), list(difference2)

filename = r'/home/atajne/terpilot/data_scraping/intermediatedata/unique_professors_planetterp.json'
data = read_from_json(filename)

grading_courses = data['grading_professors']
info_courses = data['info_professors']

intersection, removed_from_grading, removed_from_info = get_intersection_and_difference(grading_courses, info_courses)

print("Intersection: ", intersection)
print("Removed from grading_professors: ", removed_from_grading)
print("Removed from info_professors: ", removed_from_info)

# Write the intersection back to the file
data['final_list'] = intersection
write_to_json(data, filename)
