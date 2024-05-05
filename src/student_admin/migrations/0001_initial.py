# Generated by Django 5.0.2 on 2024-04-04 20:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin?')),
                ('department', models.CharField(max_length=100)),
                ('groups', models.ManyToManyField(related_name='admin_users', to='auth.group')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(related_name='admin_users_permissions', to='auth.permission')),
            ],
        ),
        migrations.CreateModel(
            name='StudentUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin?')),
                ('major', models.CharField(max_length=100)),
                ('major_ii', models.CharField(blank=True, max_length=100, null=True)),
                ('minor', models.CharField(blank=True, max_length=100, null=True)),
                ('minor_ii', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('courses', models.JSONField(default=dict)),
                ('groups', models.ManyToManyField(related_name='student_users', to='auth.group')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(related_name='student_users_permissions', to='auth.permission')),
            ],
        ),
    ]