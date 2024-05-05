
def translate_year_sem(student, selected_year_string, selected_sem_string):
    selected_year_string = int(selected_year_string)
    selected_sem_string = selected_sem_string.strip()
    print(selected_sem_string)
    print(selected_year_string)
    student_cohort = student.cohort
    selected_year = "didn't work"
    selected_sem_choice = "also didn't work"
    if selected_year_string == student_cohort: # let's say spring 2024
        if selected_sem_string == "Spring":
            selected_year ="3"
            selected_sem_choice = "1"
    elif selected_year_string == student_cohort-1: # spring 2023, fall 2023
        if selected_sem_string == "Fall":
            selected_year = "3"
            selected_sem_choice ="0"
        elif selected_sem_string == "Spring":
            selected_year = "2"
            selected_sem_choice = "1"
    elif selected_year_string == student_cohort-2: # spring 2022, fall 2022
        if selected_sem_string == "Fall":
            selected_year = "2"
            selected_sem_choice = "0"
        elif selected_sem_string == "Spring":
            selected_year = "1"
            selected_sem_choice = "1"
    elif selected_year_string == student_cohort-3: # spring 2021, fall 2021
        print("doing good")
        if selected_sem_string == "Fall":
            selected_year = "1"
            selected_sem_choice = "0"
        elif selected_sem_string == "Spring":
            print("still doing good")
            selected_year = "0"
            selected_sem_choice = "1"
    elif selected_year_string == student_cohort-4: # fall 2020
        selected_year = "0"
        selected_sem_choice = "0"

    return [selected_year, selected_sem_choice]
    # if equal to student cohort, selected_year = 3 2024
    # if equal to student cohort - 1, selected_year = 2 2023
    # if equal to student cohort -2, selected_year = 1 2022
    # if equal to student cohort -3, selected_year = 0 2021