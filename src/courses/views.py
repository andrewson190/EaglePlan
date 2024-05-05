from .models import SelectedCourse
from django.http import JsonResponse

# def select_course(request):
#     if request.method == 'POST':
#         course_key = request.POST.get('course_key')
#         # Save the selected course to the database
#         SelectedCourse.objects.create(course_code=course_key)
#         # Return a success response
#         return JsonResponse({'message': 'Successfully registered for the course'})
#     else:
#         return JsonResponse({'message': 'Invalid request'}, status=400)