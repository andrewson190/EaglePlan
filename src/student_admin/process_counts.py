from courses.models import Course



def process_counts(data, semester, year):
    # semester is either 0 or 1 for fall or spring
    # year is either 0,1,2,3 for current year, +1,2,3
    """
    Traverses the data dictionary containing course codes as keys and QuerySet objects as values.
    Processes each QuerySet entry and handles empty QuerySet objects.

    Args:
        data (dict): Dictionary with course codes as keys and QuerySet objects as values.
    """
    # Iterate through the dictionary
    display_counts = {}
    for course_code, queryset in data.items():
        course = Course.objects.get(course_code=course_code)
        course_title = course.title
        # Check if the QuerySet is not empty
        if queryset:
            # Iterate through the QuerySet to process the data
            for entry in queryset:
                entry_semester = entry.get("semester").lower().strip()
                if entry_semester == semester and entry.get('year')==year:
                    display_counts[course_code] = [entry.get('count'), course_title]
                else:
                    display_counts[course_code] = [0, course_title]
        else:
            display_counts[course_code] = [0, course_title]
    print(display_counts)
    return display_counts