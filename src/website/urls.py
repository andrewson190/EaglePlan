"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from student_admin.views import student_dashboard, login_view, admin_dashboard, student_register_view, admin_register_view
from register import views as v
from student_admin.views import student_dashboard, login_view, admin_dashboard, profile_view, plan_view, logout_view, home, redirect_view
from student_admin.views import student_dashboard, login_view, admin_dashboard, profile_view, plan_view, profile_edit_view, course_selction, unlisted_courses_view
app_name = 'website'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('', home, name="home"),
    path('student/', student_dashboard, name="student_dashboard"),
    path('admindash/', admin_dashboard, name="admin_dashboard"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('register/', v.register, name="register"),
    path('register/student/', student_register_view, name="student_register"),
    path('register/admin/', admin_register_view, name="admin_register"),
    path('redirect/student/profile/', profile_view, name = "profile_view"),
    path('redirect/student/plan/', plan_view, name = "plan_view"),
    path('redirect/student/profile/edit/', profile_edit_view, name = "profile_edit_view" ),
    path('redirect/student/course', course_selction, name = "course_selection" ),

    path('redirect/', redirect_view, name='redirect'),
    path('redirect/student/', student_dashboard, name='student_dashboard'),
    path('redirect/admindash/', admin_dashboard, name='admin_dashboard'),
    path('redirect/register/', v.register, name='register'),
    path('redirect/register/student_register/', student_register_view, name='student_register'),
    path('redirect/register/admin_register/', admin_register_view, name='admin_register'),
    path('redirect/plan/', plan_view, name="plan_view"),
    path('redirect/course/', course_selction, name="course_selection"),
    path('redirect/course/unlisted/', unlisted_courses_view, name="unlisted_courses"),
    #path('custom_redirect/', custom_redirect, name='custom_redirect_url'),
   # path('custom_redirect/admindash/', admin_dashboard, name='admin_dashboard'),
   # path('custom_redirect/student/', student_dashboard, name='student_dashboard')
]
