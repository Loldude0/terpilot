import requests
from bs4 import BeautifulSoup
from time import sleep

courses_list = []
#read from file and convert to list
with open("list.html", "r") as file: #<-------------------->CHANGE<-------------------->
    courses_list = eval(file.read())

print(courses_list)

urlpart1 = r"https://app.testudo.umd.edu/soc/search?courseId="
urlpart2 = r"&sectionId=&termId=202408&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"

for course in courses_list:
    print("completing for " + course)
    url = urlpart1 + course + urlpart2
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    with open(course + ".html", "w") as file:
        file.write(soup.prettify())