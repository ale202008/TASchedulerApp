from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserCreationForm, UserEditForm
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from TASchedulerWebApp.models import User

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
def account_info(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account_info.html', context)


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def account_creation(request):
    if request.method == 'POST':
        # Check if what type a form to create again on submit
        if "password" in dict(request.POST.items()):
            title = "Create a new user account"
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User account created successfully.')
            else:
                messages.error(request, 'An error occurred while creating the user account')
            form = UserCreationForm()
            return render(request, 'accountCreation.html', {'form': form, 'title': title})
        else:
            title = "Edit a user account"
            username = dict(request.POST.items()).get("usernameSelect")
            count = 1
            limit = int(username)
            # Iterate to get to selected Username to edit
            for user in User.objects.all():
                username = user.username
                count += 1
                if count > limit:
                    break
            try:
                a = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "This user does not exist")
                form = UserEditForm()
                return render(request, 'accountCreation.html', {'form': form, 'title': title})
            form = UserEditForm(request.POST, instance=a)
            if form.is_valid():
                form.save()
                messages.success(request, 'User account edited successfully')
            else:
                messages.error(request, "An error occurred while editing the user account")
            form = UserEditForm()
            return render(request, 'accountCreation.html', {'form': form, 'title': title})
    else:
        # Load create by default and edit when selected
        if "edit" in dict(request.GET.items()):
            title = "Edit a user account"
            form = UserEditForm()
        else:
            title = "Create a new user account"
            form = UserCreationForm()
    return render(request, 'accountCreation.html', {'form': form, 'title': title})


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
        return render(request, "CoursePage.html", {"Courses": courses, "message": ""})

    def post(self, request):
        user = request.user
        courselist = list(Course.objects.all())
        if (user.is_superuser):
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
            if(sectionnumber == ""): return render(request, "SectionPage.html", {"message1":"Section Name blank"})
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


