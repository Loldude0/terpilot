import json

# Load professor info
with open('/home/atajne/terpilot/data_scraping/professor_data_final/all_prof_info.json', 'r') as f:
    prof_info = json.load(f)

# Load summaries
with open('/home/atajne/terpilot/data_scraping/professor_data_final/summaries.json', 'r') as f:
    summaries = json.load(f)

# Load grading statistics
with open('/home/atajne/terpilot/data_scraping/professor_data_final/professor_grading_statistics.json', 'r') as f:
    grading_stats = json.load(f)

# Combine data
combined_data = []
for prof in prof_info:
    combined_prof = prof
    for summary in summaries:
        if summary['name'] == prof['name']:
            combined_prof['summary'] = summary['summary']
            break
    for grading in grading_stats:
        if grading['professor'] == prof['name']:
            combined_prof['grading'] = grading['grading']
            break
    #remove unecessary fields from prof
    combined_prof.pop('courses', None)
    combined_prof.pop('reviews', None)
    combined_prof.pop('slug', None)
    combined_prof.pop('type', None)
    combined_data.append(combined_prof)

# Write combined data to a new file
with open('/home/atajne/terpilot/data_scraping/professor_data_final/combined_prof_info.json', 'w') as f:
    json.dump(combined_data, f, indent=4)
