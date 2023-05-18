from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django import forms


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, related_name='myapp_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='myapp_user_permissions', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name


class Course(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=200)
    Instructor = models.ForeignKey('User', blank = True, null = True, on_delete = models.DO_NOTHING, related_name='Course_Instructor', unique = False)
    TeacherAssistant = models.ForeignKey('User', blank=True, null=True, on_delete=models.DO_NOTHING, related_name='Course_TeacherAssistant', unique=False)

class Section(models.Model):
    id = models.CharField(max_length=150, unique=True, primary_key=True)
    TeacherAssistant = models.ForeignKey('User', blank = True, null = True, on_delete = models.DO_NOTHING, related_name = 'Section_TeacherAssistant', unique = False)
    Instructor = models.ForeignKey('User', blank = True, null = True, on_delete = models.DO_NOTHING, related_name = 'Section_Instructor', unique = False)
    Course = models.ForeignKey('Course', blank=True, null=True, on_delete=models.CASCADE)

class Skill(models.Model):
    name = models.CharField(max_length = 69, blank = True)
    TeacherAssistant = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE, related_name='Skill_TeacherAssistant', unique=False)

class Notification(models.Model):
    notification = models.CharField(max_length = 1000)
    UserAllowed = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE, related_name='Notification_UserAllowed', unique=False)
    Sender = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE, related_name='Notification_Sender', unique=False)

class CourseAssignmentForm(forms.ModelForm):
    Course = forms.CharField(max_length=12, required=False)
    Instructor = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    TeacherAssistant = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Course
        fields = ('Course', 'Instructor', 'TeacherAssistant')
