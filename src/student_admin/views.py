from django.shortcuts import render
from .models import AdminUser
from .models import StudentUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentForm, AdminForm, ProfileForm, PlanSelectionForm, YearSemesterForm
from .models import StudentUser, AdminUser
from courses.get_courses import CourseSelection
from majors import major_manage
from courses.models import Course
from plans.models import Plan, Counts
import json
from django.core.cache import cache
from plans.plan_manage import PlanManagement
from django.db import models
from datetime import date
from .process_counts import process_counts
from .translate_year_sem import translate_year_sem


# Create your views here.
def student_dashboard(request):
    student = request.user.studentuser

    if not student.plans.exists():
        # Create instances of Plan if they don't exist already
        plan_a = Plan.objects.create(name='A')
        PlanManagement.plan_setup(plan_a)
        plan_b = Plan.objects.create(name='B')
        PlanManagement.plan_setup(plan_b)
        plan_c = Plan.objects.create(name='C')
        PlanManagement.plan_setup(plan_c)
        # Associate plans A, B, and C with the student
        student.plans.add(plan_a, plan_b, plan_c)

        # removes old courses when plans are deleted
        PlanManagement.clear_courses_taken(student)
    credits_percentage = str(round(PlanManagement.return_total_credits_taken(student)))
    major_percentage = str(round(PlanManagement.return_major_minor_percentage(student, "major")))
    minor_percentage = str(round(PlanManagement.return_major_minor_percentage(student, "minor")))
    majorI_credits = student.majorI_credits
    total_credits_taken = student.total_credits_taken
    majorII_credits = student.majorII_credits
    minorI_credits = student.minorI_credits
    minorII_credits = student.minorII_credits
    
    context = {
        'student': student,
        'credits_percentage': credits_percentage,
        'major_percentage': major_percentage,
        'minor_percentage': minor_percentage,
        'minorII_credits': minorII_credits,
        'minorI_credits': minorI_credits, 
        'majorII_credits': majorII_credits,
        'total_credits_taken': total_credits_taken,
        'majorI_credits': majorI_credits
    }
    return render(request, "landingpage.html", context)

def admin_dashboard(request):
    counts = {}
    current_year = date.today().year
    admin = request.user
    admin_user = request.user.adminuser
    dept = admin_user.department # CSCI, MATH, etc.
    queryset = Course.objects.filter(course_code__startswith=dept)
    # get course count information, stored in course_counts variable
    course_counts = {}
    for obj in queryset:

        # Queries the Counts model to get counts of courses added, grouped by semester & year
        enrollments = Counts.objects.filter(course=obj) \
            .values('semester', 'year') \
            .annotate(count=models.Count('*'))

        # Store the counts in a dictionary with the course as the key and counts as values
        course_counts[obj.course_code] = enrollments
        #count = Counts.objects.filter(course=obj, semester=0, year=0).count()

        #print("count: ", count)
    if request.method == 'POST':
        form = YearSemesterForm(request.POST)
        if form.is_valid():
            selected_year = form.cleaned_data['year']
            print("selected admin year: ", selected_year)
            selected_semester = form.cleaned_data['semester']
            print("selected admin semester: ", selected_semester)
            #if selected_semester.lower() == ("fall"):
                #selected_semester = 0
            #elif selected_semester.lower()=="spring":
                #selected_semester = 1
            #if selected_year == (str(current_year)):
                #selected_year = 0
            #elif selected_year == (str(current_year+1)):
                 #selected_year = 1
            #elif selected_year == (str(current_year+2)):
                 #selected_year = 2
            #elif selected_year == (str(current_year+3)):
                 #selected_year = 3

            counts = process_counts(course_counts, selected_semester, selected_year)

    else:
        form = YearSemesterForm()


    # You can customize the data you pass to the template here
    context = {
        'admin': admin,
        'form': YearSemesterForm,
        'counts': counts
    }
    return render(request, "admin_dashboard.html", context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to appropriate dashboard based on user type
                if user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('student_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {'form': form})

def student_register_view(request):
    try:
        student_user = request.user.studentuser
    except StudentUser.DoesNotExist:
        #isAdmin = request.POST.get("isAdmin")
        student_user = StudentUser(user=request.user,is_admin=False)
       # student_user.is_admin = True
       # student_user.save()

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student_user)
        if form.is_valid():
            student_user.is_admin=False
            form.save()
        # Redirect to the same page after successful form submission
        return redirect('student_dashboard')
    else:
        form = StudentForm(instance=student_user)
    context = {'form': form}
    return render(request, "student_register.html", context)

def admin_register_view(request):
    try:
        admin_user = request.user.adminuser
    except AdminUser.DoesNotExist:
        admin_user = AdminUser(user=request.user, is_admin=True)
        #admin_user.is_admin = False
       # admin_user.save()

    if request.method == 'POST':
        form = AdminForm(request.POST, instance=admin_user)
        if form.is_valid():
            admin_user.is_admin=True
            form.save()
        # Redirect to the same page after successful form submission
        return redirect('admin_dashboard')
    else:
        form = AdminForm(instance=admin_user)
    context = {'form': form}
    return render(request, "admin_register.html", context)

def profile_view(request):
    form = ProfileForm(request.POST or None)
    student = request.user.studentuser
    context = {
        'student': student,
        'form': form
    }
    return render(request, "profile.html", context)

def profile_edit_view(request):
    form = ProfileForm(request.POST or None)
    student = request.user.studentuser
    context = {
        'student': student,
        'form': form
    }
    return render(request, "profile_edit.html", context)

def course_selction(request): # select plan -- A,B,C -- save json to there
    student = request.user.studentuser
    cohort_year = student.cohort
    searched = get_courses_info()
    x= 'no error'

    
    #if not student.plans.exists():
        # Create instances of Plan if they don't exist already
       # plan_a= Plan.objects.create(name='A')
        #PlanManagement.plan_setup(plan_a)
       # plan_b = Plan.objects.create(name='B')
       # PlanManagement.plan_setup(plan_b)
       # plan_c = Plan.objects.create(name='C')
       # PlanManagement.plan_setup(plan_c)
        # Associate plans A, B, and C with the student
        #student.plans.add(plan_a, plan_b, plan_c)

        #removes old courses when plans are deleted
       # PlanManagement.clear_courses_taken(student)


    def search_query():
        query_dict = request.GET
        print(query_dict)
        try:
            query = query_dict.get("search_query")
        except:
            query = None
        
        if query is not None:
            searched_courses = Course.objects.filter(title__contains=query)
            return searched_courses
        else:
            return get_courses_info()
    
    def filter_by_department(department_code):
        print(department_code)
        if department_code == 'CSCI' or department_code == 'MATH':
            filtered_courses = Course.objects.filter(course_code__startswith=department_code)
        else:
            filtered_courses = Course.objects.none()
        return filtered_courses
    
    searched = search_query()
    print("HI")
    print(request.GET)
    if request.method =='GET' and "searchDept" in request.GET:
        dept = request.GET.get('searchDept')
        searched = filter_by_department(dept)

    if request.method =='GET' and "search_query" in request.GET:

        searched = search_query()


    if request.method == 'POST':
        form = PlanSelectionForm(request.POST)
        form.set_student(student)
        print("Is form valid?: ", form.is_valid())

        #print(request.POST['select']) # course code selected


        if form.is_valid():
            selected_plan = form.cleaned_data['selected_plan']
            plan = Plan.objects.get(name=f'{selected_plan}')

            selected_sem = form.cleaned_data['selected_sem']

            selected_year_string = form.cleaned_data['selected_sem'][-4:]
            selected_sem_string = form.cleaned_data['selected_sem'][:-4]
            print("selected year & sem:", selected_year_string, selected_sem_string)

            year_sem = translate_year_sem(student, selected_year_string, selected_sem_string)
            joined_year_sem = ''.join(year_sem)

            selected_courses = []
            print(request.POST['select'])
            selected_courses.append(request.POST['select']) 
            x = PlanManagement.add_courses_to_plan(selected_courses, plan, student,joined_year_sem, selected_year_string,selected_sem_string)
    else:
        form = PlanSelectionForm()
        form.set_student(student)

    print(PlanManagement.freshmen_cohort)
    courses = get_courses_info()
    context = {
        'student': student,
        'courses': courses,
        'form': form,
        'searched_courses': searched,
        'message': x
        #'form':form
    }
    return render(request, "select_courses.html", context)

def plan_view(request):
    student = request.user.studentuser
    courses = student.courses   
    plan_dicA = json.loads(Plan.objects.get(name='A').plan_dictionary) 
    plan_dicB = json.loads(Plan.objects.get(name='B').plan_dictionary) 
    plan_dicC = json.loads(Plan.objects.get(name='C').plan_dictionary) 

    for key, value in plan_dicA.items():
        if value[0] != '':
            course_title = Course.objects.get(course_code = f'{value[0]}').title
            plan_dicA[key].append(course_title)
    print(plan_dicA)

    for key, value in plan_dicB.items():
        if value[0] != '':
            course_title = Course.objects.get(course_code = f'{value[0]}').title
            plan_dicB[key].append(course_title)
    print(plan_dicA)

    for key, value in plan_dicC.items():
        if value[0] != '':
            course_title = Course.objects.get(course_code = f'{value[0]}').title
            plan_dicC[key].append(course_title)
    print(plan_dicA)

    if request.method == "POST":
        selected_course_list = []
        plan = request.POST.get('plan')
        course = request.POST.get('course')
        position = request.POST.get('position')
        print(position)

        selected_course_list.append(course)
      
        selected_plan = Plan.objects.get(name=f'{plan}')
        PlanManagement.remove_course_from_plan(selected_course_list, selected_plan, student, position)

    sort_dict = PlanManagement.sort_dict
    context = {
        'student': student,
        'courses': courses,
        'planA': plan_dicA,
        'planB': plan_dicB,
        'planC': plan_dicC,

        'sort': sort_dict
    }
    return render(request, "plan.html", context)


def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    cache.set('courses_info_loaded', True)
    if not cache.get('courses_info_loaded'):
        course_codes = ['AADS', 'ACCT', 'ADAN', 'ADCJ', 'ADCY', 'ADET', 'ADEX', 'ADHA', 'ADSA', 'ADSB', 'APSY', 'ARTH', 'ARTS', 'BCOM', 'BIOL', 'BSLW', 'BZAN', 'CHEM', 'CLAS', 'COMM', 'CSCI', 'EALC', 'ECON', 'EDUC', 'EESC', 'ELHE', 'ENGL', 'ENGR', 'ENVS', 'ERAL', 'FILM', 'FORM', 'FORS', 'FREN', 'GERM', 'GSOM', 'HIST', 'HLTH', 'ICSP', 'INTL', 'ISYS', 'ITAL', 'JESU', 'JOUR', 'LAWS', 'LING', 'LREN', 'MATH', 'MESA', 'MFIN', 'MGMT', 'MKTG', 'MUSA', 'MUSP', 'NELC', 'NURS', 'PHCG', 'PHIL', 'PHYS', 'POLI', 'PRTO', 'PSYC', 'RLRL', 'ROTC', 'SCHI', 'SCWK', 'SLAV', 'SOCY', 'SPAN', 'THEO', 'THTR', 'UGMG', 'UNAS', 'UNCP']
        for course in course_codes:
            CourseSelection.get_courses_info(course)
        # Set a flag in the cache to indicate that the courses info has been loaded
        cache.set('courses_info_loaded', True)
    major_manage.create_all_majors()

    return render(request, "home.html")

def redirect_view(request):
    user = request.user
    try:
        student_user = user.studentuser
        return redirect('student/')
    except StudentUser.DoesNotExist:
        # Handle the case where the user doesn't have a StudentUser associated
        pass
    try:
        admin_user = user.adminuser
        return redirect('admindash/')
    except AdminUser.DoesNotExist:
        # Handle the case where the user doesn't have a StudentUser associated
        pass
    return redirect('register/')

def unlisted_courses_view(request):
    student = request.user.studentuser
    context = {
        'student': student
    }
    return render(request, "unlisted_courses.html", context)


def get_courses_info():
    #courses = Course.objects.filter(course_code__icontains='CSCI')
    courses = Course.objects.all()
    return courses



