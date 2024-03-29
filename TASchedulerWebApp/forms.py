from django import forms
from .models import User
from .models import User, Course


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
    delete_account = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
        labels = {
            'email': 'Email', 'first_name': "First Name", 'last_name' : "Last Name", 'is_staff': "Instructor"
        }

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("emailSelect")
        if user == User.objects.get(email=user).email:
            raise forms.ValidationError("Email already exists")

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['delete_account']:
            user.delete()
            return None
        updatefields = []
        for field in self.cleaned_data.keys():
            if self.cleaned_data.get(field) != "" and field != "emailSelect" and field != 'delete_account':
                updatefields.append(field)
        if commit:
            user.save(update_fields=updatefields)
        return user


class NonAdminEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        labels = {
            'email': 'Email', 'first_name': "First Name", 'last_name' : "Last Name"
        }

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data["password"]
        password_confirm = self.cleaned_data["password_confirm"]
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        print(self.cleaned_data["password"])
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class CourseAssignForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    instructor = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True, is_superuser=False), to_field_name="email")
    ta = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False, is_superuser=False), to_field_name="email")



