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
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            print("logged in")
            return redirect('directory')
        else:
            messages.error(request, 'Invalid email or password')
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
            email = dict(request.POST.items()).get("emailSelect")
            count = 1
            limit = int(email)
            # Iterate to get to selected email to edit
            for user in User.objects.all():
                email = user.email
                count += 1
                if count > limit:
                    break
            try:
                a = User.objects.get(email=email)
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
        courses = list(Course.objects.all())
        if (user.is_superuser):
            if (request.POST.get('chosen') == "Add Course"):
                return render(request, "AddCoursePage.html", {"message":""})
            elif (request.POST.get('chosen') == "Delete Course"):
                return render(request, "DeleteCoursePage.html", {'Courseoptions':courses,"Courses": courses})
        if (request.POST.get('chosen') == "Home"):
            return redirect('directory')
        return render(request, 'CoursePage.html', {"Courses": courses, "message": "You are not a supervisor"})


class AddCoursePage(View):
    def get(self, request):
        return render(request, "AddCoursePage.html", {"message": ""})

    def post(self, request):
        name = request.POST.get('CourseName','')
        number = request.POST.get('CourseNumber','')
        try:
            Course.objects.get(id=number)
            return render(request, "AddCoursePage.html", {"message": "course already exists."})
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
        courses = list(Course.objects.all())
        return render(request, "DeleteCoursePage.html", {'Courseoptions':courses,'Course':courses})

    def post(self, request):

        number = request.POST.get('chosen', '')
        if number == 'Back':
            courses = list(Course.objects.all())
            return render(request, "CoursePage.html", {'Courses':courses})
        if number != '':
                course = Course.objects.get(id=number)
                course.delete()
                courses = list(Course.objects.all())
                return render(request, "CoursePage.html", {'message': 'Course deleted', 'Courses': courses})
        else:
            courses = list(Course.objects.all())
            return render(request, "DeleteCoursePage.html",
                        {'message': "Please choose a course", 'Courseoptions':courses, 'Courses': courses})


class Sections(View):
    def get(self,request):
        courses = list(Course.objects.all())
        return render(request, "SectionPage.html", {"Courseoptions":courses})

    def post(self,request):
        todo = request.POST.get('chosen')
        courses = list(Course.objects.all())

        #goes back directory page
        if todo == "Back":
            return redirect('directory')
        if todo == "Add Section":
            return render(request, "AddSectionPage.html", {"Courseoptions":courses})
        if todo == "Delete Section":
            sections = list(Section.objects.all())
            return render(request, "DeleteSectionPage.html", {"Sectionoptions":sections})
        #displays sections for a course
        number = request.POST.get('show section')
        course = Course.objects.get(id=number)
        sections = list(Section.objects.filter(Course=course))

        #checks if course has any sections
        if sections.__len__() == 0:
            return render(request, "SectionPage.html", {"message":"No section for this course", "Sections": sections, "Courseoptions": courses})
        return render(request, "SectionPage.html", {"Sections":sections, "Courseoptions": courses})



class AddSectionPage(View):
    def get(self, request):
        courses = list(Course.objects.all())
        return render(request, "AddSectionPage.html", {"Courseoptions":courses})

    def post(self, request):
        number = request.POST.get('create section', '')
        sectionnumber = request.POST.get('SectionNumber', '')
        courses = list(Course.objects.all())

        if (request.POST.get('chosen') == "Back"):
            return render(request, "SectionPage.html", {'Courseoptions':courses})

        if sectionnumber == "": return render(request, "AddSectionPage.html",
                                              {"message1": "Section Number blank", "Courseoptions": courses})

        course = Course.objects.get(id=number)

        try:
            Section.objects.get(id=sectionnumber)
            sections = list(Section.objects.filter(Course=course))
            return render(request, "AddSectionPage.html",
                          {"message1": "Section exists", "Sections": sections, "Courseoptions": courses})
        except:
            newsection = Section.objects.create(id=sectionnumber, Course=course)
            newsection.save()

            sections = list(Section.objects.filter(Course=course))
            courses = list(Course.objects.all())
            return render(request, "SectionPage.html",
                          {"message1": "Section Added", "Sections": sections, "Courseoptions": courses})



class DeleteSectionPage(View):
    def get(self, request):
        sections = list(Section.objects.all())
        return render(request, "DeleteSectionPage.html", {"Sectionoptions":sections})
    def post(self, request):
        courses = list(Course.objects.all())
        todo = request.POST.get('chosen')
        if(todo == "Back"):
            return render(request, "SectionPage.html", {'Courseoptions':courses})

        section = Section.objects.get(id=todo)
        course = section.Course
        sections = Section.objects.filter(Course=course)
        section.delete()
        return render(request, "SectionPage.html", {"Courseoptions":courses, 'Sections':sections, })