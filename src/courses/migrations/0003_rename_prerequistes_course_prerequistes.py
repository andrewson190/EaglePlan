# Generated by Django 4.1.7 on 2024-04-12 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_prerequistes_course_level_course_satisfies_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='Prerequistes',
            new_name='prerequistes',
        ),
    ]