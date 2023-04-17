from django.shortcuts import render, redirect
from django.views import View
from .models import Supervisor, Instructor, TeacherAssistant, Course, LabSection, LectureSection

# Create your views here.

class CoursePage(View):
    def get(self, request):
        courses = list(Course.objects)
        return render(request, "Course.html", {"Courses": courses})
    def post(self, request):
        sess = request.session[""]