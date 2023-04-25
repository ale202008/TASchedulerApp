from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from TASchedulerWebApp.forms import UserCreationForm
from TASchedulerWebApp.forms import InstructorForm
from TASchedulerWebApp.forms import TeachingAssistantForm
from TASchedulerWebApp.forms import CourseForm

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
        if "Create" in dict(request.POST.items()):
            print(dict(request.POST.items()))
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User account created successfully.')
                return redirect('account_creation')
            else:
                messages.error(request, 'An error occurred while creating the user account')
        elif "Edit" in dict(request.POST.items()):
            print("Edit clicked")
            username = dict(request.POST.items()).get("username")
            try:
                a = User.objects.get(username=str(username))
            except User.DoesNotExist:
                messages.error(request, "This user does not exist")
                return redirect('account_creation')
            form = UserCreationForm(request.POST, instance=a)
            if form.is_valid():
                form.save()
                messages.success(request, 'User account edited successfully')
                return redirect('account_creation')
            else:
                messages.error(request, "An error occured while editing the user account")
        else:
            form = UserCreationForm()
    else:
        form = UserCreationForm()
    return render(request, 'accountCreation.html', {'form': form})


@login_required
def Directory(request):
  user = request.user
  buttons = []
  #Admin if statement
  if user.is_superuser:
    buttons = [
      ('Courses', 'CoursePage/'),
      ('Account Info', '/account'),
      ('Notifications', '/notifications'),
      ('Sections', 'SectionPage/'),
      ('TAs', '/tas'),
      ('Instructors', '/instructors'),
      ('Create Course', 'AddCoursePage/'),
      ('Create Section', '/create_section'),
      ('Create/Edit Account', 'account_creation/'),
    ]
    #Instructor view
  elif user.is_staff:
    buttons = [
      ('Courses', 'CoursePage/'),
      ('Account Info', '/account'),
      ('Notifications', '/notifications'),
      ('Sections', 'SectionPage/'),
      ('TAs', '/tas'),
    ]
  else:
    buttons = [
      ('Courses', 'CoursePage/'),
      ('Account Info', '/account'),
      ('Notifications', '/notifications'),
      ('Sections', 'SectionPage/'),
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
        instructor_form = InstructorForm()
        teaching_assistant_form = TeachingAssistantForm()
        context = {
            "Courses": courses,
            "message": "",
            "instructor_form": instructor_form,
            "teaching_assistant_form": teaching_assistant_form,
        }
        return render(request, "CoursePage.html", {"Courses": courses, "message": ""})

    def post(self, request):
        user = request.user
        courselist = list(Course.objects.all())
        if (user.is_superuser):
            if request.POST.get("submit") == "Add Instructor":
                instructor_form = InstructorForm(request.POST)
                if instructor_form.is_valid():
                    instructor_form.save()
                    course_id = request.POST.get("course_id")
                    course = Course.objects.get(id=course_id)
                    course.instructors.add(instructor)
                    course.save()
                    messages.success(request, "Instructor added successfully.")
                else:
                    messages.error(request, "An error occurred while adding the Instructor.")
            elif request.POST.get("submit") == "Add TA":
                teaching_assistant_form = TeachingAssistantForm(request.POST)
                if teaching_assistant_form.is_valid():
                    teaching_assistant_form.save()
                    course_id = request.POST.get("course_id")
                    course = Course.objects.get(id=course_id)
                    course.teaching_assistants.add(teaching_assistant)
                    course.save()
                    messages.success(request, "Teaching Assistant added successfully.")
                else:
                    messages.error(request, "An error occurred while adding the Teaching Assistant.")
            if (request.POST.get('chosen') == "Add Course"):
                return render(request, "AddCoursePage.html", {"message":""})
            elif (request.POST.get('chosen') == "Delete Course"):
                return render(request, "DeleteCoursePage.html", {"Courses": courselist})
        if (request.POST.get('chosen') == "Home"):
            return redirect('directory')
        return render(request, 'CoursePage.html', {"Courses": courselist, "message": "You are not a supervisor"})


class AddCoursePage(View):
    def get(self, request):
        return render(request, "AddCoursePage.html", {"message": ""})

    def post(self, request):
        name = request.POST.get('CourseName','')
        number = request.POST.get('CourseNumber','')
        try:
            Course.objects.get(id=number)
            return render(request, "AddCoursePage.html", {"message": "course number already in use."})
        except:
            if (name != '' and number != ''):
                newcourse = Course.objects.create(id=number, name=name)
                newcourse.save()
                courselist = list(Course.objects.all())
                return render(request, "CoursePage.html", {"Courses": courselist, "message": "course created."})
            courselist = list(Course.objects.all())
            return render(request, "AddCoursePage.html", {"message": "course not created."})


class DeleteCoursePage(View):
    def get(self, request):
        courselist = list(Course.objects.all())
        return render(request, "DeleteCoursePage.html", {'Course':courselist})

    def post(self, request):
        name = request.POST.get('CourseName', '')
        number = request.POST.get('CourseNumber', '')
        if(name != '' and number != ''):
            try:
                course = Course.objects.get(id=number)
                course.delete()
                courses = list(Course.objects.all())
                return render(request, "CoursePage.html", {'message': 'Course deleted', 'Courses': courses})
            except:
                courses = list(Course.objects.all())
                return render(request, 'DeleteCoursePage.html',
                              {'message': "Please enter an existing course" , 'Courses': courses})
        courses = list(Course.objects.all())
        return render(request, "DeleteCoursePage.html",
                      {'message': "Please enter a course name and number", 'Courses': courses})


class Sections(View):
    def get(self,request):
        return render(request, "SectionPage.html")

    def post(self,request):
        todo = request.POST.get('chosen')
        if(todo == "Show Sections"):
            name = request.POST.get('CourseName')
            number = request.POST.get('CourseNumber')
            try:
                course = Course.objects.get(id=number, name=name)
                sections = list(course.Sections.all())
                return render(request, "SectionPage.html", {"Sections":sections})
            except:
                return render(request, "SectionPage.html", {"message":"Course doesn't exist or has no sections"})
        else:
            name = request.POST.get('CourseName')
            number = request.POST.get('CourseNumber')
            sectionnumber = request.POST.get('SectionNumber')
            try:
                course = Course.objects.get(id=number, name=name)
                try:
                    course.Sections.get(name=sectionnumber)
                    sections = list(course.Sections.all())
                    return render(request, "SectionPage.html",{"message1":"Section exists", "Sections":sections})
                except:
                    course.Sections.create(name=sectionnumber)
                    sections = list(course.Sections.all())
                    return render(request, "SectionPage.html", {"message1":"Section Added", "Sections":sections})
            except:
                return render(request, "SectionPage.html", {"message1":"Course doesn't exist or has no sections"})

class InstructorCreationView(View):
    def get(self, request):
        form = InstructorForm()  # creating an instance of InstructorForm
        return render(request, 'instructor_creation.html', {'form': form})

    def post(self, request):
        form = InstructorForm(request.POST) # creating an instance of InstructorForm with POST data
        if form.is_valid(): # checking if the form is valid
            form.save() # saving the form data
            messages.success(request, 'Instructor account created successfully.')  # displaying success message
            return redirect('instructor_creation')  # redirecting to the same page
        else:
            messages.error(request, 'An error occurred while creating the instructor account') # displaying error message
        return render(request, 'instructor_creation.html', {'form': form})  # rendering the page with the form


class TeachingAssistantCreationView(View):
    def get(self, request):
        form = TeachingAssistantForm() # creating an instance of TeachingAssistantForm
        return render(request, 'teaching_assistant_creation.html', {'form': form})

    def post(self, request):
        form = TeachingAssistantForm(request.POST) # creating an instance of TeachingAssistantForm with POST data
        if form.is_valid(): # checking if the form is valid
            form.save() # saving the form data
            messages.success(request, 'Teaching Assistant account created successfully.') # displaying success message
            return redirect('teaching_assistant_creation') # redirecting to the same page
        else:
            messages.error(request, 'An error occurred while creating the teaching assistant account') # displaying error message
        return render(request, 'teaching_assistant_creation.html', {'form': form}) # rendering the page with the form

