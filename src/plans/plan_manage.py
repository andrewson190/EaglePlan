import json
from courses.models import Course
from plans.models import Plan 
from student_admin.models import StudentUser
from majors.models import Major 
from datetime import datetime

from plans.models import Plan, Counts

class PlanManagement():
    senior_cohort = junior_cohort = sophomore_cohort = freshmen_cohort = datetime.now().year

    semester = None
    sort_dict = {'000': 0, '001': 1, '002': 2, '003': 3, '004': 4, '005': 5, '006': 6, 
                  '010': 7, '011': 8, '012': 9, '013': 10, '014': 11, '015': 12, '016': 13, 
                   '100': 14, '101': 15, '102': 16, '103': 17, '104': 18, '105': 19, '106': 20,
                     '110': 21, '111': 22, '112': 23, '113': 24, '114': 25, '115': 26, '116': 27, 
                      '200': 28, '201': 29, '202': 30, '203': 31, '204': 32, '205': 33, '206': 34, 
                       '210': 35, '211': 36, '212': 37, '213': 38, '214': 39, '215': 40, '216': 41, 
                         '300': 42, '301': 43, '302': 44, '303': 45, '304': 46, '305': 47, '306': 48, 
                          '310': 49, '311': 50, '312': 51, '313': 52, '314': 53, '315': 54, '316': 55}
    
    def __init__(self):
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.semester = 1 if self.current_month >= 6 else 2
        if self.semester == 1:
            self.senior_cohort = self.current_year + 1
            self.unior_cohort = self.current_year + 2
            self.sophomore_cohort = self.current_year + 3
            self.freshmen_cohort = self.current_year + 4
        else:
            self.senior_cohort = self.current_year
            self.junior_cohort = self.current_year + 1
            self.sophomore_cohort = self.current_year + 2
            self.freshmen_cohort = self.current_year + 3
    
    def defining_cohorts(self):
        global senior_cohort, junior_cohort, sophomore_cohort, freshmen_cohort, semester

        if self.semester == 1:
            senior_cohort = self.current_year + 1
            junior_cohort = self.current_year + 2
            sophomore_cohort = self.current_year + 3
            freshmen_cohort = self.current_year + 4
        else:
            senior_cohort = self.current_year
            junior_cohort = self.current_year + 1
            sophomore_cohort = self.current_year + 2
            freshmen_cohort = self.current_year + 3

        return senior_cohort, junior_cohort, sophomore_cohort, freshmen_cohort

    def plan_setup(plan_model):
        plan = {}
        courses = {}
        for x in range(4):
            for semster in range(2):
                for place in range(7):
                    plan_string = str(x) + str(semster) + str(place)
                    plan[plan_string] = ["", ""]
        plan = json.dumps(plan)
        courses = json.dumps(courses)
        Plan.objects.update_or_create(
                    name = plan_model.name,
                    defaults={
                        'plan_dictionary': plan,
                        'course_dictionary': courses
                    }
                )
        return
    
    def add_courses_to_plan(selected_course_list, selected_plan, student, selected_position=None, select_year=None, select_sem=None): # selected_position=None
        sort_dict = PlanManagement.sort_dict
        plan_dictionary = json.loads(selected_plan.plan_dictionary)
        course_dictionary = json.loads(selected_plan.course_dictionary)

        for course in selected_course_list: #no double register 
            if course in course_dictionary:
                return "Course {} is already in the plan".format(course)
                #if PlanManagement.double_regesiter_handling(selected_plan, course, student, "Credit"):
                #   break
                #return
                #raise ValueError("Course {} is already in the plan".format(course))

            course_dictionary = json.loads(selected_plan.course_dictionary)
            course_model = Course.objects.get(course_code=course)

            prerequisites = json.loads(course_model.prerequisites)
            corequisites = json.loads(course_model.corequisite)

            for prereq in prerequisites: #have you taken prereqs
                if prereq not in course_dictionary:
                    return "You must first take {}".format(prereq)
                    #raise ValueError("You must first take {}".format(prereq))
            
            if selected_position == None:
                for position, value in plan_dictionary.items(): #is there space in the plan for a course 
                    if value == ["", ""]:
                        plan_dictionary[position] = [course, str(course_model.credits)]
                        course_dictionary[course] = position
                        selected_plan.plan_dictionary = json.dumps(plan_dictionary)
                        selected_plan.course_dictionary = json.dumps(course_dictionary)
                        selected_plan.save()
                        PlanManagement.automatic_update_courses_taken(course, position, student)
                        print(student.courses_taken)
                        PlanManagement.specific_major_minor_adding(course, student)
                        student.save()
                        for coreq in corequisites:
                            if coreq not in course_dictionary:
                                return "You must also take {}".format(coreq)
                                #raise ValueError("You must also take {}".format(coreq))
                        break
                    else:
                        continue  # If no empty positions found, continue to the next course
            else:
                for position, value in {k: sort_dict[k] for k in sort_dict if (selected_position + '0') <= k <= (selected_position + '6')}.items():
                    if plan_dictionary[position] == ["", ""]:
                        plan_dictionary[position] = [course, str(course_model.credits)]
                        if course in course_dictionary:
                            plan_dictionary[course_dictionary[course]][1] = "RETAKEN"
                            course_dictionary[course] = [course_dictionary[course], position]
                        else:
                            course_dictionary[course] = position
                        selected_plan.plan_dictionary = json.dumps(plan_dictionary)
                        selected_plan.course_dictionary = json.dumps(course_dictionary)
                        selected_plan.save()
                        PlanManagement.automatic_update_courses_taken(course, position, student)
                        print("adding to major validation: ", student.courses_taken)
                        PlanManagement.specific_major_minor_adding(course, student)
                        PlanManagement.return_total_credits_taken(student)
                        student.save()
                        for coreq in corequisites:
                            if coreq not in course_dictionary:
                                return "You must also take {}".format(coreq)
                                #raise ValueError("You must also take {}".format(coreq))
                        break
                else:
                    return "There is no space in this semster"
                

            print("This is the core percentage: ", PlanManagement.return_core_percentage(student))
            print("This is the major percentage : ", PlanManagement.return_major_minor_percentage(student, "major"))

            if selected_plan.name == "A":
                enrollment = Counts(course=course_model, semester=select_sem, year=select_year)
                enrollment.save()


            # print("course_code", course_model.course_code)
            #print(pos)
            #print("before: ", course_model.course_count)
            #course_count_update = course_model.course_count + 1
            #print("what it should be updated to: ", course_count_update)
           # Course.objects.filter(course_code=course_model.course_code).update(
            #    course_count=course_model.course_count + 1)
            #course_model.refresh_from_db()
            #print("updated: ", course_model.course_count)

            # If a course was successfully added, break out of the loop
            break
        
        print(course_dictionary, plan_dictionary, "\n", type(plan_dictionary))
        return "no error"

    def manually_add_to_courses_taken(course, student, credits=None):
        print("they have taken: ", student.courses_taken)
        if student.courses_taken == None or student.courses_taken == '' or student.courses_taken == "{}":
            print("New dictionary")
            student.courses_taken = json.dumps({})

        courses_taken = json.loads(student.courses_taken)
        course_credits = Course.objects.get(course_code=course).credits if Course.objects.filter(course_code=course).exists() else 0

        if course not in courses_taken:
            if credits is None:
                courses_taken[course] = [course, course_credits]
            else:
                courses_taken[course] = [course, float(credits)]
        else:
            # This type of course has been taken more than once
            count = courses_taken[course][0] if isinstance(courses_taken[course][0], float) else 0
            if credits is None:
                courses_taken[course] = [count + 1, course_credits]
            else:
                courses_taken[course] = [count + 1, float(credits)]

        # Update the courses_taken field in the student object
        student.courses_taken = json.dumps(courses_taken)
        student.save()
        return
    
    def automatic_update_courses_taken(course, position, student):
        current_position = 0
        if student.courses_taken == None or student.courses_taken == '' or student.courses_taken == "{}":
            # Initialize courses_taken as an empty dictionary
            courses_taken = {}
            StudentUser.objects.update_or_create(
                    user = student.user,
                    defaults={
                        'courses_taken': json.dumps(courses_taken),
                    }
                )
            
        courses_taken = json.loads(student.courses_taken)
        if PlanManagement.semester == 1: #find the current positon based on the cohort of the student 
            current_position = (3 - (student.cohort - datetime.now().year)) * 2 * 7
        else:
            current_position = (3 - (student.cohort - datetime.now().year)) * 2 * 7 + 7
        
        if(PlanManagement.sort_dict[position] < current_position):
            if course not in courses_taken:
                if Course.objects.get(course_code = course).credits == None or Course.objects.get(course_code = course).credits == "":
                    courses_taken[course] = [course, 0]
                    print("added")
                    print(courses_taken)
                else: 
                    courses_taken[course] = [course, float(Course.objects.get(course_code = course).credits)]
                    print("ADDED")
                    print(courses_taken)
                courses_taken = json.dumps(courses_taken)
                student.courses_taken = courses_taken
                print("this is prior to core vlaidation from object: ", student.courses_taken)
                PlanManagement.core_validation(course, student)
            #else:
                 #raise ValueError("This course: ",course, " has already been added to taken course")
            student.total_credits_taken += Course.objects.get(course_code = course).credits 
        return

    def sort(position): #gives the index 
        return PlanManagement.sort_dict[position]
    
    def major_minor_taken_setup(student): #If major is CHANGED ADD CORNER CASE do another method
        print("THIS IS THE FIRST LINE OF SETUP TAKEN MAJOR")
        print(student.majorI_to_take, "Type of: ", type(student.majorI_to_take))
        if student.majorI_to_take == None or student.majorI_to_take == '' or len(student.majorI_to_take) < 3:
            student.majorI_to_take = Major.objects.get(name = student.major).major_courses

        if student.majorII_to_take == None or student.majorII_to_take == '' or len(student.majorII_to_take) < 3:
            if student.major_ii != None and student.major_ii != "":
                student.majorII_to_take = Major.objects.get(name = student.major_ii).major_courses

        if student.minorI_to_take == None or student.minorI_to_take == '' or len(student.minorI_to_take) < 3:
            print("this much is true")
            if student.minor != None and student.minor != "":
                student.minorI_to_take = Major.objects.get(name = student.minor).major_courses
            else:
                print("passing gorl")
                minorI_to_take = json.dumps({})
                student.minorI_to_take = minorI_to_take

        if student.minorII_to_take == None or student.minorII_to_take == '' or len(student.minorII_to_take) < 3:
            if student.minor_ii != None and student.minor_ii != "":
                student.minorII_to_take = Major.objects.get(name = student.minor_ii).major_courses
            else:
                minorII_to_take = json.dumps({})
                student.minorII_to_take = minorII_to_take

    def specific_major_minor_adding(course, student):
        PlanManagement.major_minor_taken_setup(student)
        #print("SPECIFIC MAJOR", student.majorI_to_take, "   ", type(student.majorI_to_take))

        majorI = student.majorI_to_take
        majorII = student.majorII_to_take
        minorI = student.minorI_to_take
        minorII = student.minorII_to_take

        if isinstance(majorI, str):
            majorI_to_take = json.loads(majorI)
        elif isinstance(majorI, dict):
            majorI_to_take = majorI
        else:
            majorI_to_take = {}

        if isinstance(majorII, str):
            majorII_to_take = json.loads(majorII)
        elif isinstance(majorII, dict):
            majorII_to_take = majorII
        else:
            majorII_to_take = {}

        if isinstance(minorI, str):
            minorI_to_take = json.loads(minorI)
        elif isinstance(minorI, dict):
            minorI_to_take = minorI
        else:
            minorI_to_take = {}

        if isinstance(minorII, str):
            minorII_to_take = json.loads(minorII)
        elif isinstance(minorII, dict):
            minorII_to_take = minorII
        else:
            minorII_to_take = {}

        if "Natural_Science" in majorI_to_take:
            for course_list in majorI_to_take["Natural_Science"]:
                if course in course_list:
                    course_list.remove(course)

                elif course[:6] in course_list:
                    course_list.remove(course[:6])

                else:
                    for element in course_list:
                        if isinstance(element, list):
                            if course[:5] in element:
                                course_list.remove(element)
                if not course_list:
                    del majorI_to_take["Natural_Science"]
            majorI_dump = json.dumps(majorI_to_take)
            student.majorI_to_take = majorI_dump

        if "Natural_Science" in majorII_to_take:
            for course_list in majorII_to_take["Natural_Science"]:
                if course in course_list:
                    course_list.remove(course)

                elif course[:6] in course_list:
                    course_list.remove(course[:6])

                else:
                    for element in course_list:
                        if isinstance(element, list):
                            if course[:5] in element:
                                course_list.remove(element)
                if not course_list:
                    del majorII_to_take["Natural_Science"]
            majorII_dump = json.dumps(majorII_to_take)
            student.majorII_to_take = majorII_dump

        if "Electives" in minorI_to_take:
            if course != "MATH2210" and course != "MATH2211" and course != "MATH2202" and course != "MATH2203" and course != "MATH2252" and course != "MATH2253":
                if course[:6] in minorI_to_take["Electives"][0]:
                    minorI_to_take["Electives"][1] -= 1
                    if minorI_to_take["Electives"][1] == 0:
                        del minorI_to_take["Electives"]
                    minorI_dump = json.dumps(minorI_to_take)
                    student.minorI_to_take = minorI_dump

        if "Electives" in minorII_to_take:
            if course != "MATH2210" and course != "MATH2211" and course != "MATH2202" and course != "MATH2203" and course != "MATH2252" and course != "MATH2253":
                if course[:6] in minorII_to_take["Electives"][0]:
                    minorII_to_take["Electives"][1] -= 1
                    if minorII_to_take["Electives"][1] == 0:
                        del minorII_to_take["Electives"]
                    minorII_dump = json.dumps(minorII_to_take)
                    student.minorII_to_take = minorII_dump

        if "Choice_1" in minorI_to_take:
            if course in minorI_to_take["Choice_1"]:
                del minorI_to_take["Choice_1"]
                minorI_dump = json.dumps(minorI_to_take)
                student.minorI_to_take = minorI_dump

        if "Choice_1" in minorII_to_take:
            if course in minorII_to_take["Choice_1"]:
                del minorII_to_take["Choice_1"]
                minorII_dump = json.dumps(minorII_to_take)
                student.minorII_to_take = minorII_dump


        #print("THIS IS THE MAJOR METHOD")
        flag_1 = False
        if course in majorI_to_take:
            if majorI_to_take[course] == 0 or isinstance(majorI_to_take[course], str):
                del majorI_to_take[course]
                flag_1 = True
            else:
                majorI_to_take[course] -= 1
                if majorI_to_take[course] == 0:
                    del majorI_to_take[course]
                    flag_1 = True
        else:
            if course[:8] in majorI_to_take:
                if majorI_to_take[course[:8]] == 0 or isinstance(majorI_to_take[course[:8]], str):
                    del majorI_to_take[course[:8]]
                    flag_1 = True
                else:
                    majorI_to_take[course[:8]] -= 1
                    if majorI_to_take[course[:8]] == 0:
                        del majorI_to_take[course[:8]]
                        flag_1 = True
            elif course[:7] in majorI_to_take:
                if majorI_to_take[course[:7]] == 0 or isinstance(majorI_to_take[course[:7]], str):
                    del majorI_to_take[course[:7]]
                    flag_1 = True
                   
                else:
                    majorI_to_take[course[:7]] -= 1
                    if majorI_to_take[course[:7]] == 0:
                        del majorI_to_take[course[:7]]
                        flag_1 = True
                    
            elif course[:6] in majorI_to_take:
                if majorI_to_take[course[:6]] == 0 or isinstance(majorI_to_take[course[:6]], str):
                    del majorI_to_take[course[:6]]
                    flag_1 = True
                    
                else:
                    majorI_to_take[course[:6]] -= 1
                    if majorI_to_take[course[:6]] == 0:
                        del majorI_to_take[course[:6]]
                        flag_1 = True
                   
            elif course[:5] in majorI_to_take:
                if majorI_to_take[course[:5]] == 0 or isinstance(majorI_to_take[course[:5]], str):
                    del majorI_to_take[course[:5]]
                    flag_1 = True
                    
                else:
                    majorI_to_take[course[:5]] -= 1
                    if majorI_to_take[course[:5]] == 0:
                        del majorI_to_take[course[:5]]
                        flag_1 = True
        
        if flag_1:
           student.majorI_credits += Course.objects.get(course_code = course).credits 
           if not majorI_to_take:
               majorI_to_take["done"] = ""
        
        majorI_to_take = json.dumps(majorI_to_take)
        student.majorI_to_take = majorI_to_take

        flag_2 = False
        if student.major_ii != None or student.major_ii != "":
            if course in majorII_to_take:
                if majorII_to_take[course] == 0 or isinstance(majorII_to_take[course], str):
                    del majorII_to_take[course]
                    flag_2 = True
                else:
                    majorII_to_take[course] -= 1
                    if majorII_to_take[course] == 0:
                        del majorII_to_take[course]
                        flag_2 = True
            else:
                if course[:8] in majorII_to_take:
                    if majorII_to_take[course[:8]] == 0 or isinstance(majorII_to_take[course[:8]], str):
                        del majorII_to_take[course[:8]]
                        flag_2 = True
                    else:
                        majorII_to_take[course[:8]] -= 1
                        if majorII_to_take[course[:8]] == 0:
                            del majorII_to_take[course[:8]]
                            flag_2 = True
                elif course[:7] in majorII_to_take:
                    if majorII_to_take[course[:7]] == 0 or isinstance(majorII_to_take[course[:7]], str):
                        del majorII_to_take[course[:7]]
                        flag_2 = True
                    else:
                        majorII_to_take[course[:7]] -= 1
                        if majorII_to_take[course[:7]] == 0:
                            del majorII_to_take[course[:7]]
                            flag_2 = True
                elif course[:6] in majorII_to_take:
                    if majorII_to_take[course[:6]] == 0 or isinstance(majorII_to_take[course[:6]], str):
                        del majorII_to_take[course[:6]]
                        flag_2 = True
                    else:
                        majorII_to_take[course[:6]] -= 1
                        if majorII_to_take[course[:6]] == 0:
                            del majorII_to_take[course[:6]]
                            flag_2 = True
                        
        if flag_2:
           student.majorII_credits += Course.objects.get(course_code = course).credits 
           if not majorII_to_take:
               majorII_to_take["done"] = ""
        majorII_to_take = json.dumps(majorII_to_take)
        student.majorII_to_take = majorII_to_take

        flag_3 = False
        if student.minor != None or student.minor != "":
            if course in minorI_to_take:
                if minorI_to_take[course] == 0 or isinstance(minorI_to_take[course], str):
                    del minorI_to_take[course]
                    flag_3 = True
                    
                else:
                    minorI_to_take[course] -= 1
                    if minorI_to_take[course] == 0:
                        del minorI_to_take[course]
                        flag_3 = True
            else:
                if course[:8] in minorI_to_take:
                    if minorI_to_take[course[:8]] == 0 or isinstance(minorI_to_take[course[:8]], str):
                        del minorI_to_take[course[:8]]
                        flag_3 = True
                    else:
                        minorI_to_take[course[:8]] -= 1
                        if minorI_to_take[course[:8]] == 0:
                            del minorI_to_take[course[:8]]
                            flag_3 = True
                elif course[:7] in minorI_to_take:
                    if minorI_to_take[course[:7]] == 0 or isinstance(minorI_to_take[course[:7]], str):
                        del minorI_to_take[course[:7]]
                        flag_3 = True
                    else:
                        minorI_to_take[course[:7]] -= 1
                        if minorI_to_take[course[:7]] == 0:
                            del minorI_to_take[course[:7]]
                            flag_3 = True
                elif course[:6] in minorI_to_take:
                    if minorI_to_take[course[:6]] == 0 or isinstance(minorI_to_take[course[:6]], str):
                        del minorI_to_take[course[:6]]
                        flag_3 = True
                    else:
                        minorI_to_take[course[:6]] -= 1
                        if minorI_to_take[course[:6]] == 0:
                            del minorI_to_take[course[:6]]
                            flag_3 = True

        if flag_3:
           student.minorI_credits += Course.objects.get(course_code = course).credits 
           if not minorI_to_take:
               minorI_to_take["done"] = ""
        minorI_to_take = json.dumps(minorI_to_take)
        student.minorI_to_take = minorI_to_take

        flag_4 = False
        if student.minor_ii != None or student.minor_ii != "":
            if course in minorII_to_take:
                if minorII_to_take[course] == 0 or isinstance(minorII_to_take[course], str):
                    del minorII_to_take[course]
                    flag_4 = True
                else:
                    minorII_to_take[course] -= 1
                    if minorII_to_take[course] == 0:
                        del minorII_to_take[course]
                        flag_4 = True
            else:
                if course[:8] in minorII_to_take:
                    if minorII_to_take[course[:8]] == 0 or isinstance(minorII_to_take[course[:8]], str):

                        del minorI_to_take[course[:8]]
                        flag_4 = True
                    else:
                        minorII_to_take[course[:8]] -= 1
                        if minorII_to_take[course[:8]] == 0:
                            del minorII_to_take[course[:8]]
                            flag_4 = True
                elif course[:7] in minorII_to_take:
                    if minorII_to_take[course[:7]] == 0 or isinstance(minorII_to_take[course[:7]], str):

                        del minorII_to_take[course[:7]]
                        flag_4 = True
                    else:
                        minorII_to_take[course[:7]] -= 1
                        if minorII_to_take[course[:7]] == 0:
                            del minorII_to_take[course[:7]]
                            flag_4 = True
                elif course[:6] in minorII_to_take:
                    if minorII_to_take[course[:6]] == 0 or isinstance(minorII_to_take[course[:6]], str):
                        del minorII_to_take[course[:6]]
                        flag_4 = True
                    else:
                        minorII_to_take[course[:6]] -= 1
                        if minorII_to_take[course[:6]] == 0:
                            del minorII_to_take[course[:6]]
                            flag_4 = True
                        
            if flag_4:
                student.minorII_credits += Course.objects.get(course_code = course).credits 
                if not minorII_to_take:
                    minorII_to_take["done"] = ""
            minorII_to_take = json.dumps(minorII_to_take)
            student.minorII_to_take = minorII_to_take
        return
    
    def return_major_minor_percentage(student, which_plan):
        PlanManagement.major_minor_taken_setup(student)
        percentage = 0
        if which_plan == "major":
            majorI_to_take = json.loads(student.majorI_to_take)
            if "done" in majorI_to_take:
                percentage = 1
            else:
                print("major:", len(majorI_to_take))
                print("major total:", len(json.loads(Major.objects.get(name = student.major).major_courses)))
                percentage = 1 - (len(majorI_to_take) / len(json.loads(Major.objects.get(name = student.major).major_courses)))
        elif which_plan == "major_ii":
            majorII_to_take = json.loads(student.majorII_to_take)
            if "done" in majorII_to_take:
                percentage = 1
            else:
                percentage = 1 - (len(majorII_to_take) / len(json.loads(Major.objects.get(name = student.major_ii).major_courses)))
        elif which_plan == "minor":
            minorI_to_take = json.loads(student.minorI_to_take)
            if "done" in minorI_to_take:
                percentage = 1
            elif student.minor:
                if student.minor:
                    percentage = 1 - (len(minorI_to_take) / len(json.loads(Major.objects.get(name = student.minor).major_courses)))
                else:
                    percentage = 0
        elif which_plan == "minor_ii":
            minorII_to_take = json.loads(student.minorII_to_take)
            if "done" in minorII_to_take:
                percentage = 1
            elif student.minor_ii:
                percentage = 1 - (len(minorII_to_take) / len(json.loads(Major.objects.get(name = student.minor_ii).major_courses)))
            else:
                percentage = 0
        print("This is the percentage: ", percentage * 100)

        return percentage * 100
     
    def core_validation(course, student): #figures
        print("This is before manually adding method ", student.courses_taken)
        print(type(json.loads(Course.objects.get(course_code = course).satisfies)))
        print(json.loads(Course.objects.get(course_code = course).satisfies))
        if "Core" in json.loads(Course.objects.get(course_code = course).satisfies):
            """for core_id in json.loads(Course.objects.get(course_code = course).satisfies)["Core"]:
                print("this is the core", core_id)"""
            PlanManagement.manually_add_to_courses_taken(json.loads(Course.objects.get(course_code = course).satisfies)["Core"], student)
        return

    def return_core_percentage(student):
        courses_taken = json.loads(StudentUser.objects.get(user=student.user).courses_taken)
        count = 0
        if courses_taken:
            for core in json.loads(Major.objects.get(name="Core Requirements").major_courses):
                if core in courses_taken:
                    count = count + 1
                    # Check if the course is taken
                    if (core == "ss" or core == "ns") and json.loads(Major.objects.get(name="Core Requirements").major_courses)[core] == 2:  # Checking if the first element is a string
                        count += 1
        if count == 0:
            return 0 
        return (count / 12) * 100  # Assuming there are 12 core courses in total

    def update_credits(student, credits, which):
        if not which:
            student.total_credits_taken = student.total_credits_taken + credits
        else:
            if which == "major":
                student.majorI_credits = student.majorI_credits + credits
            elif which == "major_ii":
                student.majorII_credits = student.majorII_credits + credits
            elif which == "minor":
                student.minorI_credits = student.minorI_credits + credits
            elif which == "minor_ii":
                student.minorI_credits = student.minorI_credits + credits
        return


    def double_regesiter_handling(selected_plan, course, student, what_type): #used if they failed or withdrew, want to retake (Pass/Fail), 
        courses_taken = json.loads(student.courses_taken)

        if what_type == "No Credit": #failed or withdrew
            if course in courses_taken:
                del courses_taken[course]
                PlanManagement.major_reverification(course, student)
                #manually add to plan again need to workout course dictionary
            
        if what_type == "Credit": #pass_fail
            if course in courses_taken:
                pass_fail = course + " P/F"
                print("THIS IS NEW KEY: ", pass_fail)
                courses_taken[pass_fail] = courses_taken.pop(course)
                PlanManagement.major_reverification(course, student)
                #manually add to plan again

        if what_type == "Remove":
            PlanManagement.remove_course_from_plan([course], selected_plan, student)
            return True
        
        print(courses_taken)
        student.courses_taken = json.dumps(courses_taken)
        student.save()
        return False
        

    def major_reverification(course, student):
        PlanManagement.major_minor_taken_setup(student)

        if Major.objects.filter(name=student.major).exists():
            if course in json.loads(Major.objects.get(name=student.major).major_courses):
                majorI_to_take = json.loads(student.majorI_to_take)
                majorI_to_take[course] = ""
                student.majorI_to_take = json.dumps(majorI_to_take)

        if Major.objects.filter(name=student.major_ii).exists():
            if course in json.loads(Major.objects.get(name=student.major_ii).major_courses):
                majorII_to_take = json.loads(student.majorII_to_take)
                majorII_to_take[course] = ""
                student.majorI_to_take = json.dumps(majorI_to_take)

        if Major.objects.filter(name=student.minor).exists():
            if course in json.loads(Major.objects.get(name=student.minor).major_courses):
                minorI_to_take = json.loads(student.minorI_to_take)
                minorI_to_take[course] = ""
                student.majorI_to_take = json.dumps(majorI_to_take)

        if Major.objects.filter(name=student.minor_ii).exists():
            if course in json.loads(Major.objects.get(name=student.minor_ii).major_courses):
                minorII_to_take = json.loads(student.minorII_to_take)
                minorII_to_take[course] = ""
                student.majorI_to_take = json.dumps(majorI_to_take)
        
        student.save()
        return



    def return_total_credits_taken(student):
        if not student.courses_taken:
            student.courses_taken = json.dumps({})
            student.save()
        courses_taken = json.loads(student.courses_taken)
        credits = 0
        print("THIS IS TOTAL CREDITS", type(courses_taken))
        print(courses_taken)
        for course in courses_taken.values():
            print(course)
            credits = credits + course[1]
        print(credits)
        if credits >= 120:
            return 100
        
        print((credits/120) *100)
        return (credits/120) *100

            

    def remove_course_from_plan(selected_course_list, selected_plan, student, position = None):
        plan_dictionary = json.loads(selected_plan.plan_dictionary)
        course_dictionary = json.loads(selected_plan.course_dictionary)
        courses_taken = json.loads(student.courses_taken)

        if position:
            if not selected_course_list[0]:
                print("Course", course, "not found in the plan")
                return
            course = selected_course_list[0]
            if position in plan_dictionary:
                plan_dictionary[position] = ["", ""]
                del course_dictionary[course]
                selected_plan.plan_dictionary = json.dumps(plan_dictionary)
                selected_plan.course_dictionary = json.dumps(course_dictionary)
                selected_plan.save()
            if course in courses_taken:
                del courses_taken[course]
                student.courses_taken = json.dumps(courses_taken)
                student.save()
            else:
                print("Course", course, "not found in the plan")
            return
        else:
            for course in selected_course_list:
                print(course)
                print(course_dictionary)
                if course in course_dictionary:
                    position = course_dictionary[course]
                    print(position)
                    if position in plan_dictionary:
                        plan_dictionary[position] = ["", ""]
                        del course_dictionary[course]
                        selected_plan.plan_dictionary = json.dumps(plan_dictionary)
                        selected_plan.course_dictionary = json.dumps(course_dictionary)
                        selected_plan.save()
                    if course in courses_taken:
                        del courses_taken[course]
                        student.courses_taken = json.dumps(courses_taken)
                        student.save()
                    else:
                        print("Position not found for course", course)
                else:
                    print("Course", course, "not found in the plan")
            return
    
    def clear_courses_taken(student):
        courses_taken = {}
        major_minor = json.dumps({})
        StudentUser.objects.update_or_create(
                    user = student.user,
                    defaults={
                        'courses_taken': json.dumps(courses_taken),
                        'majorI_to_take': major_minor,
                        'majorII_to_take': major_minor,
                        'minorI_to_take': major_minor,
                        'minorII_to_take': major_minor,
                        'minorII_credits': 0,
                        'minorI_credits': 0,
                        'majorII_credits': 0,
                        'total_credits_taken': 0,
                        'majorI_credits': 0
                    }
                )
        return

    

            
""" def planlol():
        plan = {}
        for x in range(4):
            for semster in range(2):
                for place in range(7):
                    plan_string = str(x) + str(semster) + str(place)
                    plan[plan_string] = ["Course code", "credits"]
        plan = json.dumps(plan)
        print(plan)
        return

def joinwords(selected_words, selected_plan): # save to plan instead
    course_dict = getattr(selected_plan, 'courses', '{}') # Get the existing course data
    for word in selected_words: 
        if word in course_dict:
            print("already in plan")
        else:
            course_dict[word] = course_dict.get(word, 0) + 1
    selected_plan.courses = course_dict  # Assign the updated dictionary directly
    selected_plan.save()
    print(selected_plan.courses)"""


"""    def check():
        current_month = datetime.now().month
        current_year = datetime.now().year
        semsterlol = None
        senior_cohort = None
        junior_cohort = None

        if (current_month >= 6):
            semsterlol = 1
        else: 
            semsterlol = 2
        
        #defining cohorts
        if (semsterlol == 1):
            senior_cohort = current_year + 1
            junior_cohort = current_year + 2
        else:
            senior_cohort = current_year 
            junior_cohort = current_year + 1
        
        print(senior_cohort, junior_cohort)
        return"""

#PlanManagement.check_dictory('01')

""""def check_dictory(selected_position):
        sort_dict = PlanManagement.sort_dict
        print(selected_position + '0')
        print(selected_position + '6')
        for key, value in {k: sort_dict[k] for k in sort_dict if (selected_position + '0') <= k <= (selected_position + '6')}.items():
                    print(key, value)"""