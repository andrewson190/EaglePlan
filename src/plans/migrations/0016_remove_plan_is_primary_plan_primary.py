# Generated by Django 5.0.2 on 2024-04-25 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0015_alter_counts_semester_alter_counts_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='is_primary',
        ),
        migrations.AddField(
            model_name='plan',
            name='primary',
            field=models.CharField(default='A', max_length=1),
        ),
    ]
