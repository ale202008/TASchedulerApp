from django.shortcuts import render, redirect
from django.views import View
from TASchedulerWebApp.models import *

# Create your views here.

class CoursePage(View):
    def get(self, request):
        courses = list(Course.objects)
        return render(request, "CoursePage.html", {"Courses": courses, "message": ""})
    def post(self, request):
        username = request.session["username"]
        print(username)
        user = User.objects.get(name=username)
        if(isinstance(user, Supervisor)):
            if(request.POST.get('name') == "Add Course"):
                return redirect("AddCoursePage.html")
            elif(request.POST.get('name') == "Delete Course"):
                return redirect("DeleteCoursePage.html")
        return render(request, "CoursePage.html", {"Couses": list(Course.objects), "message": "You are not a supervisor"})

class AddCoursePage(View):
    def get(self, request):
        return render(request, "AddCoursePage.html",{"message":""})

    def post(self, request):
        name = request.POST.get('CourseName')
        number = request.Post.get('CourseNumber')
        if(name != '' & number != ''):
           newcourse = Course.objects.create(id=number, name=name)
           newcourse.save()
        return render("CoursePage.html",{"Course":list(Course.objects), "message":"course created."})
