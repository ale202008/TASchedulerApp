from django import forms
from .models import User

from .models import Course


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

#Defining form to add an instructor
class InstructorForm(forms.ModelForm):
    # Set the model and fields to use in the form
    class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'email')
      # Set the widget for the role field to be hidden
      widgets = {'role': forms.HiddenInput()}

    # Initialize the form
    def __init__(self, *args, **kwargs):
      super(InstructorForm, self).__init__(*args, **kwargs)
      self.fields['role'] = forms.CharField(initial='INSTRUCTOR', widget=forms.HiddenInput())
    # Save the form data to the database
    def save(self, commit=True):
      # Create a user object from the form data
      user = super(InstructorForm, self).save(commit=False)
      # Set the users role to 'INSTRUCTOR'
      user.role = 'INSTRUCTOR'
      if commit:
        user.save()
      # Return the user object
      return user


class TeachingAssistantForm(forms.ModelForm):
  # Set the model and fields to use in the form
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    # Set the widget for the role field to be hidden
    widgets = {'role': forms.HiddenInput()}

  # Initialize the form
  def __init__(self, *args, **kwargs):
    super(TeachingAssistantForm, self).__init__(*args, **kwargs)
  # set the value of the role field to 'TA'
    self.initial['role'] = 'TA'

# Define a form to add a course
class CourseForm(forms.ModelForm):
  # Set the model and fields to use in the form
  class Meta:
    model = Course
    fields = ('id', 'name', 'instructors', 'teaching_assistants', 'sections')