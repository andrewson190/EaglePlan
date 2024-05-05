# Generated by Django 5.0.2 on 2024-04-19 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0011_rename_courses_plan_course_dictionary_and_more'),
        ('student_admin', '0009_rename_plan_studentuser_plans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentuser',
            name='plans',
        ),
        migrations.AddField(
            model_name='studentuser',
            name='plans',
            field=models.ManyToManyField(to='plans.plan'),
        ),
    ]
