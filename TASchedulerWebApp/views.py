from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserCreationForm

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
      return redirect('account_creation')
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
      return redirect('account_creation')
    else:
      messages.error(request, 'An error occurred while creating the user account')

  else:
    form = UserCreationForm()

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
  return render(request, 'accountCreation.html', {'form': form})

class Home(View):
  def get(self, request):
    return render(request, 'home.html')

class CoursePage(View):
    def get(self, request):
        courses = list(Course.objects)
        return render(request, "/CoursePage/", {"Courses": courses, "message": ""})
    def post(self, request):

        if(request.POST.get('name') == "Add Course"):
            return redirect("AddCoursePage.html")
        elif(request.POST.get('id') == "Delete Course"):
            return redirect("DeleteCoursePage.html")
        if(request.POST.get('id') == "Back"):
            return redirect("Home.html")
        return render(request, "/CoursePage/", {"Couses": list(Course.objects), "message": "You are not a supervisor"})

class AddCoursePage(View):
    def get(self, request):
        return render(request, "/AddCoursePage/",{"message":""})

    def post(self, request):
        name = request.POST.get('CourseName')
        number = request.Post.get('CourseNumber')
        if(name != '' & number != ''):
           newcourse = Course.objects.create(id=number, name=name)
           newcourse.save()
        return render("/CoursePage/", {"Courses": list(Course.objects), "message": "course created."})
