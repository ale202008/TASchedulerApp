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
from TASchedulerWebApp.models import *
from TASchedulerWebApp.forms import *
from .models import Course
from django.contrib.auth import get_user_model
User = get_user_model()

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
        instructors = User.objects.filter(is_staff=True, is_superuser=False)
        tas = User.objects.filter(is_staff=False, is_superuser=False)
        print("Courses:", courses)
        print("Instructors:", instructors)
        print("TAs:", tas)
        return render(request, "CoursePage.html", {"Courses": courses, "message": "", "Instructors": instructors, "TAs": tas})

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
        form = CourseAssignForm(request.POST)
        if form.is_valid():
            course = Course.objects.get(id=request.POST.get('course'))
            instructor = form.cleaned_data['instructor'] if form.cleaned_data['assign_instructor'] else None
            ta = form.cleaned_data['ta'] if form.cleaned_data['assign_ta'] else None
            course.instructor = instructor
            course.teacher_assistant = ta
            course.save()
            return redirect('coursepage')

        instructors = User.objects.filter(is_staff=True, is_superuser=False)
        tas = User.objects.filter(is_staff=False, is_superuser=False)
        return render(request, 'CoursePage.html',
                      {"Courses": courses, "message": "You are not a supervisor", "instructors": instructors,
                       "tas": tas})

    def assign_course_staff(request):
        if request.method == "POST":
            course_id = request.POST.get('course_id')
            course = Course.objects.get(id=course_id)

            instructor_id = request.POST.get('instructor_id')
            instructor = User.objects.get(id=instructor_id)

            ta_id = request.POST.get('ta_id')
            ta = User.objects.get(id=ta_id)

            course.Instructor = instructor
            course.TeacherAssistant = ta
            course.save()
            return render(request, "CoursePage.html", {"Courses": courses, "message": "Staff assigned successfully."})

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
        if(number != ''):
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
        #goes back directory page
        if todo == "Back":
            return redirect('directory')
        #displays sections for a course
        if todo == "Show Sections":
            number = request.POST.get('show section')
            try:
                course = Course.objects.get(id=number)
                sections = list(Section.objects.filter(Course=course))
                courses = list(Course.objects.all())

                #checks if course has any sections
                if sections.__len__() == 0:
                    return render(request, "SectionPage.html", {"message":"No section for this course", "Sections": sections, "Courseoptions": courses})

                return render(request, "SectionPage.html", {"Sections":sections, "Courseoptions": courses})
            except:
                courses = list(Course.objects.all())
                return render(request, "SectionPage.html", {"message":"Course doesn't exist or has no sections", "Courseoptions": courses})
        #creates a section
        else:
            number = request.POST.get('create section', '')
            sectionnumber = request.POST.get('SectionNumber', '')

            courses = list(Course.objects.all())
            if sectionnumber == "": return render(request, "SectionPage.html", {"message1": "Section Number blank", "Courseoptions": courses})

            try:
                course = Course.objects.get(id=number)

                try:
                    Section.objects.get(id=sectionnumber, Course=course)
                    sections = list(Section.objects.filter(Course=course))
                    return render(request, "SectionPage.html",{"message1":"Section exists", "Sections":sections, "Courseoptions": courses})
                except:
                    newsection = Section.objects.create(id=sectionnumber, Course=course)
                    newsection.save()

                    sections = list(Section.objects.filter(Course=course))
                    courses = list(Course.objects.all())
                    return render(request, "SectionPage.html", {"message1":"Section Added", "Sections":sections, "Courseoptions": courses})
            except:
                courses = list(Course.objects.all())
                return render(request, "SectionPage.html", {"message1":"Course doesn't exist", "Courseoptions": courses})


class AssignSection(View):
    def get(self, request):
        # Similar to what Benji did for creating sections. Will need to select a course to get sections.
        course_list = list(Course.objects.all())
        return render(request, "AssignSection.html", {"course_list": course_list})

    def post(self, request):
        todo = request.POST.get('chosen')
        course_list = list(Course.objects.all())
        # Will go through different if conditionals to decide which operation to do.
        # Copied from SectionPage code in presenting the information to the user.
        if todo == "Back":
            return redirect('directory')
        elif todo == "Show Sections":
            course_num = request.POST.get('select_course')
            # Got rid of the try/catch block as it seems there might be too many exceptions to cover in one
            # to simplify until necessary, code will run without try block.
            course = Course.objects.get(id = course_num)
            course_sections = list(Section.objects.filter(Course = course))
            if course_sections.__len__() == 0:
                return render(request, "AssignSection.html", {'message': 'No sections exist for this course.', 'Sections': course_sections, 'course_list': course_list})
            else:
                # If course sections list is not 0, meaning that we do have a section that exists we shall send back
                # the list of Instructor and Teacher Assistant users to be listed and chosen to assign.
                teacher_assistant_list = list(User.objects.filter(is_superuser = False, is_staff = False))
                instructors_list = list(User.objects.filter(is_superuser = False, is_staff = True))
                if teacher_assistant_list.__len__() == 0:
                    return render(request, "AssignSection.html", {'message': 'There exists no Teacher Assistants'})
                elif instructors_list.__len__() == 0:
                    return render(request, "AssignSection.html", {'message': 'There exists no Instructors'})
                else:
                    return render(request, 'AssignSection.html', {'course_sections': course_sections, 'teacher_assistant_list': teacher_assistant_list, 'instructor_list': instructors_list})
        elif todo == 'Assign':
            # Getting the model objects so that I can change section fields for Instructors and Teacher Assistants
            # if necessary
            section = Section.objects.get(id = request.POST.get('select_section'))
            instructor = User.objects.get(first_name= request.POST.get('select_instructor'))
            teacher_assistant = User.objects.get(first_name = request.POST.get('select_teacher_assistant'))


            # Checks to see if that section's Instructor field contains the instructor selected, will probably
            # change it so that only this course's instructor shows up
            if section.Course.Instructor != instructor:
                return render(request, "AssignSection.html", {'message2': 'Instructor does not teach this sections course', 'course_list': course_list})
            # Checks to see if the selected TA existed for a section already
            elif Section.objects.filter(TeacherAssistant = teacher_assistant).exists():
                return render(request, "AssignSection.html",{'message2': 'Teacher Assistant is already assigned to a section','course_list': course_list})
            else:
                section.Instructor = instructor
                section.TeacherAssistant = teacher_assistant
                section.save()
                return render(request, "AssignSection.html",{'message2': 'Assign successful for section: ' + section.id, 'course_list': course_list})

        return render(request, "AssignSection.html")