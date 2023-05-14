"""
URL configuration for djangoProject2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TASchedulerWebApp.views import *
from django.urls import path
import TASchedulerWebApp.views as views
urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('Directory', Directory, name="directory"),
    path('admin/', admin.site.urls),
    path('account_creation/', account_creation, name='account_creation'),
    path('home/', Home.as_view(), name='home'),
    path('CoursePage/', CoursePage.as_view(), name='coursepage'),

    path('AddCoursePage/', AddCoursePage.as_view()),
    path('DeleteCoursePage/', DeleteCoursePage.as_view()),
    path('SectionPage/', Sections.as_view()),
    path('assign_section/', AssignSection.as_view(), name='assign_section'),
    path('assign-course/', views.assign_course, name='assign_course'),

    # New URL for account information page for the account info
    path('account/', account_info, name='account_info'),
    path('user_list/', user_list, name='user_list'),

]
