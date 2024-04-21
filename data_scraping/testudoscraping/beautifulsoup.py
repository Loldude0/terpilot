import requests
from bs4 import BeautifulSoup

#<-------------------->CHANGE<-------------------->
#<-------------------->CHANGE<-------------------->
url = "https://app.testudo.umd.edu/soc/gen-ed/202408/CMSC"
#<-------------------->CHANGE<-------------------->
#<-------------------->CHANGE<-------------------->

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

#save to a file
temp = ""

with open("list.html", "w") as file: #<-------------------->CHANGE<-------------------->
    course_ids = [course["id"] for course in soup.find_all("div", class_="course")]
    #sort
    course_ids.sort()

    file.write(str(course_ids))