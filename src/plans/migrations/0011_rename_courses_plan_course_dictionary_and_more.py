# Generated by Django 4.2.10 on 2024-04-16 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0010_remove_plan_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='courses',
            new_name='course_dictionary',
        ),
        migrations.AddField(
            model_name='plan',
            name='plan_dictionary',
            field=models.JSONField(default=dict),
        ),
    ]