# Generated by Django 4.1.7 on 2023-04-26 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TASchedulerWebApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='Sections',
        ),
        migrations.AddField(
            model_name='section',
            name='Course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TASchedulerWebApp.course'),
        ),
    ]
