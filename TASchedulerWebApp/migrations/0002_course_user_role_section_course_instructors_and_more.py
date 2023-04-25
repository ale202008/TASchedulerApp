# Generated by Django 4.2 on 2023-04-25 05:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TASchedulerWebApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('INSTRUCTOR', 'Instructor'), ('TA', 'Teaching Assistant'), ('STUDENT', 'Student')], default='STUDENT', max_length=12),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('Course', models.ManyToManyField(to='TASchedulerWebApp.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(blank=True, limit_choices_to={'role': 'INSTRUCTOR'}, related_name='courses_taught', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='sections',
            field=models.ManyToManyField(blank=True, related_name='courses', to='TASchedulerWebApp.section'),
        ),
        migrations.AddField(
            model_name='course',
            name='teaching_assistants',
            field=models.ManyToManyField(blank=True, limit_choices_to={'role': 'TA'}, related_name='courses_assisted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='Courses',
            field=models.ManyToManyField(blank=True, to='TASchedulerWebApp.course'),
        ),
    ]
