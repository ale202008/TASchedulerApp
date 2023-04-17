from django.shortcuts import render, redirect
from django.views import View
from .models import Supervisor, Instructor, TeacherAssistant, Course, LabSection, LectureSection

class Directory(View):
    def get(self, request):
        return render(request, "directory.html",{})
    def post(self, request):
        return render(request, "directory.html", {})