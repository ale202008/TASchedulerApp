from django.db import migrations, models

class Migration(migrations.Migration):
    # Specify that this migration depends on the previous '0002_course_user_role_section_course_instructors_and_more' migration
    dependencies = [
        ('TASchedulerWebApp', '0002_course_user_role_section_course_instructors_and_more'),
    ]
    # Define the operation to add a new field 'role' to the 'User' model in the 'TASchedulerWebApp' app
    operations = [
        migrations.AddField(
            model_name='user', # specify the model name
            name='role', # specify the name of the new field to be added
            field=models.CharField(default='', max_length=50),  # specify the type and default value of the new field
            preserve_default=False, # specify whether to preserve existing default values
        ),
    ]
