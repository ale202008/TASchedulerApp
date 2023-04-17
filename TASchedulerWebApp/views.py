from django.shortcuts import render, redirect
from django.views import View
from TASchedulerWebApp.models import Supervisor, Instructor, TeacherAssistant, Course, LabSection, LectureSection

# Create your views here.

class CoursePage(View):
    def get(self, request):
        courses = list(Course.objects)
        return render(request, "Course.html", {"Courses": courses, "message":""})
    def post(self, request):
        user = request.session["name"]
        if(isinstance(user, Supervisor)):
            if(request == "Add Course"):
                return redirect("AddCoursePage.html")
            else:
                return redirect("DeleteCoursePage.html")
        return render(request, "CoursePage.html", {"Couses": list(Course.objects),"message":"You are not a supervisor"})


class AddCoursePage(View):
    def get(self, request):
        return render(request, "AddCoursePage.html")

    def post(self, request):
        name = request.POST.get('CourseName', '')
        number = request.Post.get('CourseNumber', '')
        if(name != '' & number != ''):
            Supervisor.createCourse(name, number)
