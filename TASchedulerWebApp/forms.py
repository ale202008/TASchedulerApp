from django import forms
from .models import User
from .models import Course, Instructor
class UserCreationForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'is_staff')

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

  class AssignInstructorForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Course')
    instructor = forms.ModelChoiceField(queryset=Instructor.objects.all(), label='Instructor')