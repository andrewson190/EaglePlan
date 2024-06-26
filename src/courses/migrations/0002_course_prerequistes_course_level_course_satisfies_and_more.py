# Generated by Django 4.1.7 on 2024-04-12 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Prerequistes',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='satisfies',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='course',
            name='time_offered',
            field=models.TextField(default=''),
        ),
    ]
