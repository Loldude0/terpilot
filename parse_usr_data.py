from tika import parser
import re

raw = parser.from_file("unofficial transcript.pdf")

start_index = raw['content'].find("Historic Course Information")
end_index = raw['content'].find("Current Course Information")

query_string = raw['content'][start_index:end_index]


class_taken = re.findall(r"[A-Z]{4}[0-9]{3}[A-Z]?", query_string)
print(class_taken)