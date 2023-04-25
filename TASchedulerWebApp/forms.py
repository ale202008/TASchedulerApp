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
    class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'email')
      widgets = {'role': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
      super(InstructorForm, self).__init__(*args, **kwargs)
      self.fields['role'] = forms.CharField(initial='INSTRUCTOR', widget=forms.HiddenInput())

    def save(self, commit=True):
      user = super(InstructorForm, self).save(commit=False)
      user.role = 'INSTRUCTOR'
      if commit:
        user.save()
      return user


class TeachingAssistantForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    widgets = {'role': forms.HiddenInput()}

  def __init__(self, *args, **kwargs):
    super(TeachingAssistantForm, self).__init__(*args, **kwargs)
    self.initial['role'] = 'TA'


class CourseForm(forms.ModelForm):
  class Meta:
    model = Course
    fields = ('id', 'name', 'instructors', 'teaching_assistants', 'sections')