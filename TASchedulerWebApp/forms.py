from django import forms
from .models import User


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


class UserEditForm(forms.ModelForm):
    usernameSelect = forms.ModelChoiceField(queryset=User.objects.all())
    username = forms.CharField(required=False, widget=forms.TextInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("usernameSelect")
        if user == User.objects.get(username=user).username:
            raise forms.ValidationError("Username already exists")

    def save(self, commit=True):
        user = super().save(commit=False)
        updatefields = []
        for field in self.cleaned_data.keys():
            if self.cleaned_data.get(field) != "" and field != "usernameSelect":
                updatefields.append(field)
        if commit:
            user.save(update_fields=updatefields)
        return user
