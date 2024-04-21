from tika import parser
import re

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