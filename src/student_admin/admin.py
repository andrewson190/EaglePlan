from django.contrib import admin
from .models import StudentUser, AdminUser

# Register your models here.
admin.site.register(AdminUser)
admin.site.register(StudentUser)