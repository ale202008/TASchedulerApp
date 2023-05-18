from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from TASchedulerWebApp.models import User
from .forms import CourseAssignForm
from django.shortcuts import render, redirect

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
    skills = Skill.objects.filter(TeacherAssistant=user)
    context = {'user': user, 'skills' : skills}
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
            limit = int(email) if email else 0
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
def account_editor(request):
    if request.method == 'POST':
        user = request.user
        email = user.email
        try:
            a = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "This user does not exist")
            form = NonAdminEditForm()
            return render(request, 'accountEdit.html', {'form': form})
        form = NonAdminEditForm(request.POST, instance=a)
        users = User.objects.filter(email__exact=form.fields["email"])
        if users:
            if users["email"] != email:
                messages.error(request, "Email already exists")
                return render(request, 'accountEdit.html', {'form': form})
        if form.is_valid():
            form.save()
            messages.success(request, 'User account edited successfully. Please log on again.')
            return redirect("login")
        messages.error(request, "An error occurred while editing the user account")
        return render(request, 'accountEdit.html', {'form': form})
    else:
        form = NonAdminEditForm(instance=request.user)
        return render(request, 'accountEdit.html', {'form': form})

@login_required
def Directory(request):
  user = request.user
  buttons = []
  #Admin if statement
  if user.is_superuser:
    buttons = [
      ('Courses', 'CoursePage/'),
      ('Account Info', '/account'),
      ('Notifications', 'Notification/'),
      ('Sections', 'SectionPage/'),
      ('TAs', 'TAPublicInfo/'),
      ('Instructors', 'InPublicInfo/'),
      ('Create/Edit Account', 'account_creation/'),
    ]
    #Instructor view
  elif user.is_staff:
    buttons = [
      ('Courses', 'CoursePage/'),
      ('Account Info', '/account'),
      ('Notifications', 'Notification/'),
      ('Sections', 'SectionPage/'),
      ('TAs', 'TAPublicInfo/'),
      ('Instructors', 'InPublicInfo/'),
      ('Edit Account', 'account_edit/'),
    ]
  else:
    buttons = [
      ('Courses', 'CoursePage/'),
      ('Account Info', '/account'),
      ('Notifications', 'Notification/'),
      ('Sections', 'SectionPage/'),
      ('TAs', 'TAPublicInfo/'),
      ('Edit Account', 'account_edit/'),
    ]
    
  options = {'buttons': buttons}
  return render(request, 'directory.html', options)

class Home(View):
    def get(self, request):
        return render(request, 'home.html')

class CoursePage(View):
    def get(self, request):
        # Get all courses, instructors, and TAs from the database
        courses = Course.objects.all()
        Instructor = User.objects.filter(is_staff=True, is_superuser=False)
        TeacherAssistant = User.objects.filter(is_staff=False, is_superuser=False)
        form = CourseAssignForm()
        return render(request, "CoursePage.html",
                      {"Courses": courses, "Instructors": Instructor, "TAs": TeacherAssistant, "form": form})

    def post(self, request):
        form = CourseAssignForm(request.POST)
        user = request.user
        courses = list(Course.objects.all())
        if user.is_superuser:
            if request.POST.get('chosen') == "Add Course":
                return render(request, "AddCoursePage.html", {"message":""})
            elif request.POST.get('chosen') == "Delete Course":
                return render(request, "DeleteCoursePage.html", {'Courseoptions':courses,"Courses": courses})
            if form.is_valid():
                course_id = form.cleaned_data['course'].id
                instructor_id = form.cleaned_data['instructor'].id
                ta_id = form.cleaned_data['ta'].id

                try:
                    course = Course.objects.get(id=course_id)
                    instructor = User.objects.get(id=instructor_id)
                    ta = User.objects.get(id=ta_id)

                    if Course.objects.filter(Instructor=instructor).exists():
                        message = 'This instructor is already assigned to the course.'
                    elif Course.objects.filter(TeacherAssistant=ta).exists():
                        message = 'This TA is already assigned to the course.'
                    else:
                        course.Instructor = instructor
                        course.TeacherAssistant = ta

                        course.save()
                        message = 'Assignment successful'
                except (Course.DoesNotExist, User.DoesNotExist):
                    message = 'Course not found or user not found'

            courses = Course.objects.all()
            instructors = User.objects.filter(is_staff=True, is_superuser=False)
            tas = User.objects.filter(is_staff=False, is_superuser=False)

            return render(request, 'CoursePage.html',
                          {"Courses": courses, "Instructors": instructors, "TAs": tas, "form": form,
                           "message": message})

        Courses = Course.objects.all()
        Instructor = User.objects.filter(is_staff=True, is_superuser=False)
        TeacherAssistant = User.objects.filter(is_staff=False, is_superuser=False)

        return render(request, 'CoursePage.html',
                      {"Courses": Courses, "Instructors": Instructor, "TAs": TeacherAssistant, "form": form,
                       "message": "Failed to assign, please try again"})


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
                courses = list(Course.objects.all())
                return render(request, "CoursePage.html", {"Courses":courses, "message":"Course created"})
            return render(request, "AddCoursePage.html", {"message": "course not created."})


class DeleteCoursePage(View):
    def get(self, request):
        courses = list(Course.objects.all())
        return render(request, "DeleteCoursePage.html", {'Courseoptions':courses,'Course':courses})

    def post(self, request):
        number = request.POST.get('chosen', '')
        if number != '':
                course = Course.objects.get(id=number)
                course.delete()
                return redirect("CoursePage")
        else:
            courses = list(Course.objects.all())
            return render(request, "DeleteCoursePage.html",
                        {'message': "Please choose a course", 'Courseoptions':courses, 'Courses': courses})


class Sections(View):
    def get(self, request):
        courses = list(Course.objects.all())
        table = False
        return render(request, "SectionPage.html", {"Courseoptions":courses, 'table_bool': table})


    def post(self, request):
        todo = request.POST.get('chosen')
        courses = list(Course.objects.all())
        table = True
        if todo == "Add Section":
            return render(request, "AddSectionPage.html", {"Courseoptions": courses})
        if todo == "Delete Section":
            sections = list(Section.objects.all())
            return render(request, "DeleteSectionPage.html", {"Sectionoptions": sections})
        if todo == "Assign Section":
            return redirect('assign_section')
        # displays sections for a course
        number = request.POST.get('show section')
        if number == "":
            courses = list(Course.objects.all())
            return render(request, "SectionPage.html", {"Courseoptions": courses, "message": "Please choose a course"})
        course = Course.objects.get(id=number)
        sections = list(Section.objects.filter(Course=course))

        # checks if course has any sections
        if sections.__len__() == 0:
            return render(request, "SectionPage.html", {"message":"No section for this course", "Sections": sections, "Courseoptions": courses})
        return render(request, "SectionPage.html", {"Sections":sections, "Courseoptions": courses, 'table_bool': table})


class AddSectionPage(View):
    def get(self, request):
        courses = list(Course.objects.all())
        return render(request, "AddSectionPage.html", {"Courseoptions":courses})

    def post(self, request):
        number = request.POST.get('create section', '')
        sectionnumber = request.POST.get('SectionNumber', '')
        courses = list(Course.objects.all())
        if number == "":
            return render(request, "AddSectionPage.html",
                          {"message1": "Please choose a course", "Courseoptions": courses})
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
        if(todo == ""):
            sections = list(Section.objects.all())
            return render(request, "DeleteSectionPage.html", {"Sectionoptions":sections, "message":"Please choose a section."})
        section = Section.objects.get(id=todo)
        course = section.Course
        sections = Section.objects.filter(Course=course)
        section.delete()
        return render(request, "SectionPage.html", {"Courseoptions":courses, 'Sections':sections, })


class AssignSection(View):
    def get(self, request):
        # Similar to what Benji did for creating sections. Will need to select a course to get sections.
        return render(request, "AssignSection.html", {"course_list": self.get_courses()})

    def post(self, request):
        todo = request.POST.get('chosen')
        # Will go through different if conditionals to decide which operation to do.
        # Copied from SectionPage code in presenting the information to the user.
        if todo == "Back":
            return redirect('directory')
        elif todo == "Show Sections":
            course_num = request.POST.get('select_course')
            # Got rid of the try/catch block as it seems there might be too many exceptions to cover in one
            # to simplify until necessary, code will run without try block.
            course = Course.objects.get(id = course_num)
            if Section.objects.filter(Course = course).exists() == False:
                return render(request, "AssignSection.html", {'course_list': self.get_courses(), 'message': 'no sections'})
            course_sections = self.get_course_sections(course)
            teacher_assistant_list = self.get_teacher_assistants()
            instructors_list = self.get_course_instructors(course)
            return self.validifiy_conditions(request, course_sections, teacher_assistant_list, instructors_list)
        if todo == 'Assign':
            # Getting the model objects so that I can change section fields for Instructors and Teacher Assistants
            # if necessary
            section = Section.objects.get(id = request.POST.get('select_section'))
            instructor = self.set_instructor(request.POST.get('select_instructor'))
            teacher_assistant = self.set_teacher_assistant(request.POST.get('select_teacher_assistant'))
        return self.assign_section(request, instructor, section, teacher_assistant)


    def validifiy_conditions(self, request, course_sections, teacher_assistant_list, instructors_list):
        if self.is_Empty(course_sections):
            message = "No sections for this course"
            return render(request, "AssignSection.html", {'message': message, 'Sections': course_sections,
                                                          'course_list': self.get_courses()})
        else:
            # If course sections list is not 0, meaning that we do have a section that exists we shall send back
            # the list of Instructor and Teacher Assistant users to be listed and chosen to assign.
            if self.is_Empty(teacher_assistant_list):
                message = "There exists no Teacher Assistants"
                return render(request, "AssignSection.html", {'message': message})
            elif self.is_Empty(instructors_list):
                message = 'There exists no Instructors'
                return render(request, "AssignSection.html", {'message': message})
            else:
                return render(request, 'AssignSection.html', {'course_sections': course_sections,
                                                              'teacher_assistant_list': teacher_assistant_list,
                                                              'instructor_list': instructors_list,
                                                              'course_list': self.get_courses()})
    def set_instructor(self, select_instructor):
        if select_instructor == "":
            return None
        return User.objects.get(email=select_instructor)

    def set_teacher_assistant(self, select_teacher_assistant):
        if select_teacher_assistant == "":
            return None
        return User.objects.get(email=select_teacher_assistant)
    def get_courses(self):
        # Gets and return a list of all courses.
        course_list = list(Course.objects.all())
        return course_list

    def get_course_sections(self, course):
        course_section_list = list(Section.objects.filter(Course = course))
        return course_section_list

    def get_course_instructors(self, course):
        instructors_list = list(User.objects.filter(email = course.Instructor.email))
        return instructors_list

    def get_teacher_assistants(self):
        teacher_assistant_list = list(User.objects.filter(is_superuser=False, is_staff=False))
        return teacher_assistant_list

    def is_Empty(self, list):
        if not bool(list):
            return True
        return False


    def assign_section(self, request, instructor, section, teacher_assistant):
        # Checks to see if that section's Instructor field contains the instructor selected, will probably
        # change it so that only this course's instructor shows up
        message = ''
        # context = {'message2': message, 'course_sections': self.get_course_sections(course),
        #            'teacher_assistant_list': self.get_teacher_assistants(),
        #            'instructor_list': self.get_course_instructors(course),
        #            'course_list': self.get_courses()}

        context = {'message2': message, 'course_list': self.get_courses()}
        if instructor != None and section.Course.Instructor != instructor:
            message = 'Instructor does not teach this sections course'
            context['message2'] = message
            return render(request, "AssignSection.html", context)
        # Checks to see if the selected TA existed for a section already
        elif teacher_assistant != None and Section.objects.filter(TeacherAssistant=teacher_assistant).exists():
            message = 'Teacher Assistant is already assigned to a section'
            context['message2'] = message
            return render(request, "AssignSection.html", context)
        else:
            section.Instructor = instructor
            section.TeacherAssistant = teacher_assistant
            section.save()
            message = 'Assign successful for section: ' + section.id
            context['message2'] = message
            return render(request, "AssignSection.html", context)


class Notifications(View):
    def get(self, request):
        self.User = request.user
        return self.display_render(self.User, request, "")
    def post(self, request):
        self.User = request.user
        todo = request.POST.get('chosen')
        if todo == "Back":
            return redirect('directory')
        else:
            Users = request.POST.getlist('select_user')
            if bool(Users) == False:
                context = 'Please select recipients.'
                return self.display_render(self.User, request, context)
            notification = request.POST.get('new_notification')
            self.makeNotification(Users, notification)
            context = 'Notification sent!'
        return self.display_render(self.User, request, context)

    def display_render(self, User, request, context):
        if User.is_superuser == True:
            return render(request, 'notifications.html',
                          {'notifications': self.getNotifications(self.User), 'permission': True,
                           'instructors': self.getInstructors(), 'teacherassistants': self.getTeacherAssistants(),
                           'super_user': True, 'message': context})
        elif User.is_staff == True:
            return render(request, 'notifications.html',
                          {'notifications': self.getNotifications(self.User), 'permission': True,
                           'teacherassistants': self.getTeacherAssistants(), 'super_user': False,
                           'message': context})
        else:
            return render(request, 'notifications.html', {'notifications': self.getNotifications(self.User),
                                                          'permission': False})
    def getInstructors(self):
        instructor_list = list(User.objects.filter(is_staff=True))
        return instructor_list

    def getTeacherAssistants(self):
        teacher_assistant_list = list(User.objects.filter(is_staff=False, is_superuser=False))
        return teacher_assistant_list

    def getNotifications(self, User):
        notification_list  = list(Notification.objects.filter(UserAllowed = User))
        return notification_list

    def makeNotification(self, list, notification):
        for i in list:
            if i == 'All Instructors':
                Recipients = self.getInstructors()
                for i in Recipients:
                    self.notification = Notification.objects.create(notification=notification, UserAllowed=i, Sender = self.User)
            elif i == 'All Teacher Assistants':
                Recipients = self.getTeacherAssistants()
                for i in Recipients:
                    self.notification = Notification.objects.create(notification=notification, UserAllowed=i, Sender = self.User)
            else:
                Recipients = User.objects.get(email = i)
                self.notification = Notification.objects.create(notification=notification, UserAllowed=Recipients, Sender = self.User)
            self.notification.save()
    
def add_skill(request):
    if request.method == 'POST':
        skill_name = request.POST['skill_name']
        user = request.user
        new_skill = Skill(name=skill_name, TeacherAssistant=user)
        new_skill.save()
        return redirect('account_info')
    else:
        return redirect('account_info')
        return redirect('account_info')


class TAPublicContact(View):

    def get(self, request):
        ta = User.objects.filter(is_staff='False')
        skills = Skill.objects.all()
        return render(request, 'TAPublicInfo.html', {"tas": ta, "skills": skills})


class InPublicContact(View):

    def get(self, request):
        instructors = User.objects.filter(is_staff='True', is_superuser='False')
        return render(request, 'InPublicContact.html', {"instructor": instructors})



def assign_course(request):
    if request.method == 'POST':
        form = CourseAssignForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data.get('course')
            instructor = form.cleaned_data.get('instructor')
            teacher_assistant = form.cleaned_data.get('teacher_assistant')

            if instructor:
                course.Instructor = instructor

            if teacher_assistant:
                course.TeacherAssistant = teacher_assistant

            course.save()
            return redirect('course_page')  # replace 'course_page' with the name of your course page view
    else:
        form = CourseAssignForm()

    return render(request, 'assign_course.html',
                  {'form': form})  # replace 'assign_course.html' with the name of your HTML file

