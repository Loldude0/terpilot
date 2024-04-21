import json

def get_unique_locations(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    unique_locations = set()
    for course in data:
        try:
            for section in course['sections']:
                locations = section['locations'].split('|')
                for location in locations:
                    unique_locations.add(location.strip())
        except:
            continue

    #remove numbers from each string and then remove duplicates then sort
    unique_locations = sorted(list(set([location.split(' ')[0] for location in unique_locations])))
    return unique_locations

file_path = '/home/atajne/terpilot/data_scraping/locationsanalyzer/list.json'
print(get_unique_locations(file_path))
