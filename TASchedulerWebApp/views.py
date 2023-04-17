from django.shortcuts import render, redirect
from django.views import View
from .models import Supervisor, Instructor, TeacherAssistant, Course, LabSection, LectureSection

class Directory(View):
    def get(self, request):
        return render(request, "directory.html",{})
    def post(self, request):
        if 'redirect1_HTML' == request.POST.get('subject'):
            return redirect('/redirect1/')
        return render(request, "directory.html", {})

class Redirect1(View):
    def get(self, request):
        return render(request, "redirect1.html",{})
    def post(self, request):
        return render(request, "redirect1.html", {})