# Generated by Django 4.1.7 on 2024-04-21 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_admin', '0008_studentuser_courses_taken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentuser',
            name='total_credits_in_plan',
        ),
        migrations.AddField(
            model_name='studentuser',
            name='majorII_to_take',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='studentuser',
            name='majorI_to_take',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='studentuser',
            name='minorII_to_take',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='studentuser',
            name='minorI_to_take',
            field=models.JSONField(default=dict),
        ),
    ]