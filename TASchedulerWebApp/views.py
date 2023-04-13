from django.shortcuts import render, redirect
from django.views import View
from .models import Supervisor, Instructor, \
    TeacherAssistant, Course, LabSection, LectureSection

# Create your views here.
class Course(View):

    def get(self, request):
        return render(request, "course.html", {})

    def post(self, request):