# Generated by Django 5.0.2 on 2024-04-19 20:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0011_rename_courses_plan_course_dictionary_and_more'),
        ('student_admin', '0006_studentuser_cohort'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentuser',
            name='plans',
        ),
        migrations.AddField(
            model_name='studentuser',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='plans.plan'),
        ),
    ]
