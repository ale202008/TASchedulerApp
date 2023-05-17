# Generated by Django 4.2 on 2023-05-17 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TASchedulerWebApp', '0004_course_instructor_course_teacherassistant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='Sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Notification_Sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
