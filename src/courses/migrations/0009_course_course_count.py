# Generated by Django 5.0.2 on 2024-04-19 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_selectedcourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_count',
            field=models.IntegerField(default=0),
        ),
    ]
