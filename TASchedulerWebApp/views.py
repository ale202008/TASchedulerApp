from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserCreationForm
from django.http import HttpResponse
from .models import *


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("logged in")
            return redirect('directory')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def account_creation(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User account created successfully.')
            return redirect('account_cr')
        else:
            messages.error(request, 'An error occurred while creating the user account')
    else:
        form = UserCreationForm()
  else:
    form = UserCreationForm()

@login_required
def Directory(request):
  user = request.user
  buttons = []
  #Admin if statement
  if user.is_superuser:
    buttons = [
      ('Courses', '/courses'),
      ('Account Info', '/account'),
      ('Notifications', '/notifications'),
      ('Sections', '/sections'),
      ('TAs', '/tas'),
      ('Instructors', '/instructors'),
      ('Create Course', '/create_course'),
      ('Create Section', '/create_section'),
      ('Create Account', '/create_account'),
    ]
    #Instructor view
  elif user.is_staff:
    buttons = [
      ('Courses', '/courses'),
      ('Account Info', '/account'),
      ('Notifications', '/notifications'),
      ('Sections', '/sections'),
      ('TAs', '/tas'),
    ]
  else:
    buttons = [
      ('Courses', '/courses'),
      ('Account Info', '/account'),
      ('Notifications', '/notifications'),
      ('Sections', '/sections'),
      ('TAs', '/tas'),
    ]
    
  options = {'buttons': buttons}
  return render(request, 'directory.html', options)
 

class Home(View):
    def get(self, request):
        return render(request, 'home.html')


class CoursePage(View):
    def get(self, request):
        courses = list(Course.objects.all())
        return render(request, "CoursePage.html", {"Courses": courses, "message": ""})

    def post(self, request):
        user = request.user
        if (user.is_superuser):
            if (request.POST.get('chosen') == "Add Course"):
                return render(request, "AddCoursePage.html", {"message":""})
            elif (request.POST.get('chosen') == "Delete Course"):
                return redirect("/DeleteCoursePage/")
        if (request.POST.get('chosen') == "Back"):
            return redirect("/Directory/")
        courselist = list(Course.objects.all())
        return render(request, 'CoursePage.html', {"Courses": courselist, "message": "You are not a supervisor"})


class AddCoursePage(View):
    def get(self, request):
        return render(request, "AddCoursePage.html", {"message": ""})

    def post(self, request):
        name = request.POST.get('CourseName','')
        number = request.POST.get('CourseNumber','')
        if (name != '' and number != ''):
            newcourse = Course.objects.create(id=number, name=name)
            newcourse.save()
            courselist = list(Course.objects.all())
            return render(request, "CoursePage.html", {"Courses": courselist, "message": "course created."})
        courselist = list(Course.objects.all())
        return render(request, "AddCoursePage.html", {"message": "course not created."})
