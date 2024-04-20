import json
from bs4 import BeautifulSoup
import re

with open("list.html", "r") as file: #<-------------------->CHANGE<-------------------->
    courses_list = eval(file.read())

for course in courses_list:
    with open(course + ".html", "r") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
    
    print(course)

    try:
        course_data = {}
        course_data['course_name'] = soup.find('span', {'class': 'course-title'}).text.replace('\n', '').strip()
        course_data['course_number'] = soup.find('div', {'class': 'course-id'}).text.replace('\n', '').strip()
        course_data['credits'] = soup.find('span', {'class': 'course-min-credits'}).text.replace('\n', '').strip()
        grading_method = soup.find_all('span', {'class': 'grading-method'})
        grading_method_text = list(set([method.text.replace('\n', '').strip() for method in grading_method]))
        grading_method_text_2 = ""
        for method in grading_method_text:
            grading_method_text_2 += method + ", "
        course_data['grading_method'] = grading_method_text_2.replace('\n', '').strip()
        approved_course = soup.find_all('div', {'class': 'approved-course-text'})
        approved_course_text = [course.text.replace('\n', '').strip() for course in approved_course]
        if 'Prerequisite:' in approved_course_text[0]:
            course_data['prereq'] = re.sub('\s+', ' ', approved_course_text[0].split('Prerequisite:', 1)[1].split('.')[0].replace('\n', '').strip())
        if 'Corequisite:' in approved_course_text[0]:
            course_data['coreq'] = re.sub('\s+', ' ', approved_course_text[0].split('Corequisite:', 1)[1].split('.')[0].replace('\n', '').strip())
        if 'Restriction:' in approved_course_text[0]:
            course_data['restriction'] = re.sub('\s+', ' ', approved_course_text[0].split('Restriction:', 1)[1].split('.')[0].replace('\n', '').strip())
        course_data['description'] = re.sub('\s+', ' ', approved_course_text[1].replace('\n', '').strip())
        geneds = soup.find_all('span', {'class': 'course-subcategory'})
        geneds_text = list(set([gened.text.replace('\n', '').strip() for gened in geneds]))
        course_data['geneds'] = geneds_text

        sections = soup.find_all('div', {'class': 'section delivery-f2f'})
        sections_data = []
        for section in sections:
            section_data = {}
            section_data['section_id'] = section.find('span', {'class': 'section-id'}).text.replace('\n', '').strip()
            section_data['professor'] = section.find('span', {'class': 'section-instructor'}).text.replace('\n', '').strip()
            section_data['total_seats'] = section.find('span', {'class': 'total-seats-count'}).text.replace('\n', '').strip()
            section_data['open_seats'] = section.find('span', {'class': 'open-seats-count'}).text.replace('\n', '').strip()
            section_data['waitlist'] = section.find('span', {'class': 'waitlist-count'}).text.replace('\n', '').strip()
            times = section.find('div', {'class': 'class-days-container'}).find_all('div', {'class': 'section-day-time-group push_two five columns'})
            section_data['times'] = ' | '.join([time.find('span', {'class': 'section-days'}).text.replace('\n', '').strip() + ' ' + time.find('span', {'class': 'class-start-time'}).text.replace('\n', '').strip() + '-' + time.find('span', {'class': 'class-end-time'}).text.replace('\n', '').strip() for time in times])
            sections_data.append(section_data)

            course_data['sections'] = sections_data

        with open(course + '.json', 'w') as outfile:
            json.dump(course_data, outfile)
    except:
        print("Error in parsing " + course + ".html")
        continue
