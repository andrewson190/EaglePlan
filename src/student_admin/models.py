from django.db import models
from django.contrib.auth.models import AbstractUser, User
from plans.models import Plan

class AdminUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False, verbose_name='Admin?')
    department = models.CharField(max_length=100)
    # Add related_name for groups and user_permissions

class StudentUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    plans = models.ManyToManyField(Plan)
    is_admin = models.BooleanField(default=False, verbose_name='Admin?')
    major = models.CharField(max_length=100)
    major_ii = models.CharField(max_length=100, blank=True, null=True)
    minor = models.CharField(max_length=100, blank=True, null=True)
    minor_ii = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    courses = models.JSONField(default=dict)
    cohort = models.IntegerField(default=None, blank=True, null=True)
    #Major Validation
    courses_taken = models.JSONField(default=dict) #will have course code as key and credits as value
    majorI_to_take = models.JSONField(default=dict)
    majorI_credits = models.FloatField(default=0)

    majorII_to_take = models.JSONField(default=dict)
    majorII_credits = models.FloatField(default=0)

    minorI_to_take = models.JSONField(default=dict)
    minorI_credits = models.FloatField(default=0)

    minorII_to_take = models.JSONField(default=dict)
    minorII_credits = models.FloatField(default=0)

    total_credits_taken = models.FloatField(default=0)
    