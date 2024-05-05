from django.db import models
from courses.models import Course
from django.contrib.auth.models import User

class Plan(models.Model):
    name = models.CharField(max_length=1)
    plan_dictionary = models.JSONField(default=dict)
    course_dictionary = models.JSONField(default=dict)

class Counts(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.CharField(max_length=10)
    year = models.CharField(max_length=4)

    def course_code(self):
        return self.course.course_code


