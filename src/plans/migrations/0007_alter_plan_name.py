# Generated by Django 5.0.2 on 2024-04-13 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0006_remove_plan_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.CharField(max_length=1),
        ),
    ]
