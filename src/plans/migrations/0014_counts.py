# Generated by Django 5.0.2 on 2024-04-19 23:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_course_course_count'),
        ('plans', '0013_delete_studentcounts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.IntegerField()),
                ('year', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='courses.course')),
            ],
        ),
    ]