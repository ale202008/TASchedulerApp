from django import forms
from .models import User, Course
from .models import InstructorTA

from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_staff')
        labels = {
            'email': 'Email', 'first_name': "First Name", 'last_name' : "Last Name", 'is_staff': "Instructor"
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    emailSelect = forms.ModelChoiceField(queryset=User.objects.all())
    email = forms.EmailField(required=False, widget=forms.TextInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
        labels = {
            'email': 'Email', 'first_name': "First Name", 'last_name' : "Last Name", 'is_staff': "Instructor", 'is_active' : "Administrator"
        }
    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("emailSelect")
        if user == User.objects.get(email=user).email:
            raise forms.ValidationError("Email already exists")

    def save(self, commit=True):
        user = super().save(commit=False)
        updatefields = []
        for field in self.cleaned_data.keys():
            if self.cleaned_data.get(field) != "" and field != "emailSelect":
                updatefields.append(field)
        if commit:
            user.save(update_fields=updatefields)
        return user

class CourseForm(forms.ModelForm):
    instructors = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True, is_superuser=False), required=False)
    teacher_assistants = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False, is_superuser=False), required=False)
    assign_instructor = forms.BooleanField(required=False)
    assign_ta = forms.BooleanField(required=False)

    class Meta:
        model = Course
        fields = ['instructors', 'teacher_assistants', 'assign_instructor', 'assign_ta']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'] = forms.ModelChoiceField(queryset=Course.objects.all())

class InstructorTAModelForm(forms.ModelForm):
    class Meta:
        model = InstructorTA
        fields = [ 'email', 'course']


class CourseAssignForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    instructor = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True, is_superuser=False))
    ta = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False, is_superuser=False))

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        instructor = cleaned_data.get('instructor')
        ta = cleaned_data.get('ta')

        if course and instructor and ta:
            if instructor in course.instructors.all():
                raise forms.ValidationError('This instructor is already assigned to the course.')

            if ta in course.teacher_assistants.all():
                raise forms.ValidationError('This TA is already assigned to the course.')

    def save(self):
        course = self.cleaned_data['course']
        instructor = self.cleaned_data['instructor']
        ta = self.cleaned_data['ta']

        course.instructors.add(instructor)
        course.teacher_assistants.add(ta)
        course.save()