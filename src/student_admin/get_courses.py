import requests
import json
import re


class CourseSelection():
    def joinwords(selected_words, student):
        course_data = getattr(student, 'courses', '{}') # Get the existing course data
        course_dict = course_data 
        for word in selected_words: 
            if  course_dict[word] == None:
                course_dict[word] = course_dict.get(word, 0) + 1
            else:
                print("already in plan")
        student.courses = course_dict  # Assign the updated dictionary directly
        student.save()
        print(student.courses)
    
    def get_courses_info(code = "CSCI"): #This gets 20 courses with a random code
        url = "http://localhost:8080/planning/planningcourses"
        params = {"code": code}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json() # Parse the JSON response
            for course_data in data[:]:  # Process only the first 20 responses
                print(course_data, "\n\n")
                course_info = course_data['course']
                title = course_info.get('title', "Title Not Available")
                print(title)
                description = course_info['descr']['plain']
                print(description)
                course_code = course_info['courseCode']
                print(course_code)
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
                print(prerequisite)
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
                print(corequisite)
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
                            if 'F' in enabler.get('startAtpId', ''):
                                time_offered = 'F'
                                break
                            elif 'S' in enabler.get('startAtpId', ''):
                                time_offered = 'S'
                                break
                if time_offered is None:
                    time_offered = 'B'
                print(time_offered)
                credits = None
                if 'creditOptionIds' in course_data['course']:
                    credit_options = course_data['course'].get('creditOptionIds', [])
                    for x in credit_options:
                        match = re.match(r".*([0-9]\.[0-9]+)$", x)
                        if match:
                            credits = float(match.group(1))
                            print(credits)
                        else:
                            print("No 'creditOptionIds' found in the course data.")
                else:
                    print("No 'creditOptionIds' found in the course data.")
                level = None
                match = re.search(r"\d", course_code)
                if match:
                    level = int(match.group(0)) * 1000
                else:
                    level = None
                print(level)
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
                print(satisfies)
        else:
            print("help")
        return 
    
    
    
CourseSelection.get_courses_info()