from django import forms
from .models import User

from .models import User, Course
from .models import Instructor

class UserCreationForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'role')

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

# Define a form to add an instructor to a course
class CourseInstructorForm(UserCreationForm):
  course = forms.ModelChoiceField(queryset=Course.objects.all())

  def save(self, commit=True):
    # Get the course object from the form
    course = self.cleaned_data['course']

    # Create a user object from the form data
    user = super().save(commit=False)

    # Set the users role to 'INSTRUCTOR'
    user.role = 'INSTRUCTOR'

    if commit:
      # Save the user object
      user.save()

      # Add the user to the course's instructors
      course.instructors.add(user)

    # Return the user object
    return user

# Define a form to add a teaching assistant
class TeachingAssistantForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    widgets = {'role': forms.HiddenInput()}

  def __init__(self, *args, **kwargs):
    super(TeachingAssistantForm, self).__init__(*args, **kwargs)
    self.initial['role'] = 'TA'

# Define a form to add a course
class CourseForm(forms.ModelForm):
  class Meta:
    model = Course
    fields = ('id', 'name', 'instructors', 'teaching_assistants', 'sections')