from django.db import models

class Course(models.Model):
    course_count = models.IntegerField(default=0)
    course_code = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    prerequisites = models.JSONField(default=dict)
    time_offered = models.TextField(default=None) #should be F,S or B
    satisfies = models.JSONField(default=dict) #for major or core
    corequisite = models.JSONField(default=dict)

    
class SelectedCourse(models.Model):
    course_code = models.CharField(max_length=10)
    # You can add more fields as needed, such as user_id or plan_id