# Generated by Django 4.1.7 on 2024-04-19 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_admin', '0007_studentuser_total_credits_in_plan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentuser',
            name='courses_taken',
            field=models.JSONField(default=dict),
        ),
    ]
