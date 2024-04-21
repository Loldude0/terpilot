import summarizer
import sys

def generate_summaries(directory):
    summaries = []
    for filename in glob.glob(os.path.join(directory, "*.json")):
        with open(filename, "r") as file:
            print(f"Generating summary for {filename}")
            professor_info = json.load(file)
            summaries.append(generate_summary_for_professor(professor_info))
            sleep(5)

    # Write the summaries to a new JSON file
    with open("summaries.json", "w") as file:
        json.dump(summaries, file, indent=4)

generate_summaries("/home/atajne/terpilot/data_scraping/planetterp_data/professor_info")