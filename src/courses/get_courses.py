from .models import Course
import re
import json
import requests

class CourseSelection():
    def get_courses_info(code):
        url = "http://localhost:8080/planning/planningcourses"
        params = {"code": code}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            for course_data in data[0:]:
                course_info = course_data['course']
                title = course_info.get('title', "Title Not Available")
                description = course_info['descr']['plain']
                course_code = course_info['courseCode']
                prerequisite = {}
                if 'prereqTerseTranslations' in course_data:
                    for prer in course_data['prereqTerseTranslations']:
                        if 'translation' in prer:
                            prerequisite_holder = prer['translation']['plain']
                            pattern = r'\b[A-Z]{4}\s?\d{4}\b'
                            matches = re.findall(pattern, prerequisite_holder)
                            matches = [match.replace(" ", "") for match in matches]
                            for match in matches:
                                prerequisite[match] = ""
                            break
                prerequisite = json.dumps(prerequisite)
                corequisite ={}
                if 'coreqTerseTranslations' in course_data:
                    for coreq in course_data['coreqTerseTranslations']:
                        if 'translation' in coreq:
                            coreq_holder = coreq['translation']['plain']
                            pattern = r'\b[A-Z]{4}\s?\d{4}\b'
                            matches = re.findall(pattern, coreq_holder)
                            matches = [match.replace(" ", "") for match in matches]
                            for match in matches:
                                corequisite[match] = ""
                            break
                corequisite = json.dumps(corequisite)
                time_offered = None
                if 'offeringEnablers' in course_data:
                    for enabler in course_data['offeringEnablers']:
                        if enabler['atpTypeKeys']:
                            if '.fall' in enabler['atpTypeKeys']:
                                time_offered = 'F'
                                break
                            elif '.spring' in enabler['atpTypeKeys']:
                                time_offered = 'S'
                                break
                        if time_offered == None:
                            try:
                                if 'F' in enabler.get('startAtpId', ''):
                                    time_offered = 'F'
                                    break
                                elif 'S' in enabler.get('startAtpId', ''):
                                    time_offered = 'S'
                                    break
                            except: 
                                break
                if time_offered is None:
                    time_offered = 'B'
                credits = None
                if 'creditOptionIds' in course_data['course']:
                    credit_options = course_data['course'].get('creditOptionIds', [])
                    for x in credit_options:
                        match = re.match(r".*([0-9]\.[0-9]+)$", x)
                        if match:
                            credits = float(match.group(1))
                level = None
                match = re.search(r"\d", course_code)
                if match:
                    level = int(match.group(0)) * 1000
                satisfies = {}
                for requirement in course_data['requirements']:
                    if requirement.get('name') == 'Major Requirements':
                        satisfies['Major'] = course_code[0:4] + str(level)
                    if requirement.get('name') == 'Minor Requirements':
                        satisfies['Minor'] = course_code[0:4] + str(level)
                    if requirement.get('name') == 'Elective Requirements':
                        satisfies['Elective'] = course_code[0:4] + str(level)
                    if requirement.get('type') == 'kuali.requirement.type.core':
                        satisfies['Core'] = requirement.get('id') 
                satisfies = json.dumps(satisfies)
                Course.objects.update_or_create(
                    course_code=course_code,
                    defaults={
                        'title': title,
                        'description': description,
                        'credits': credits,   
                        'level': level,
                        'prerequisites': prerequisite,
                        'time_offered': time_offered,
                        'corequisite': corequisite,
                        'satisfies': satisfies,
                     }
                 )
        else:
            print("help")
        return