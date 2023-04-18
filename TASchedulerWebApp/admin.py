from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Supervisor)
admin.site.register(TeacherAssistant)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(LabSection)
admin.site.register(LectureSection)