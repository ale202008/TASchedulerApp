# Import necessary modules
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

# Define a custom manager for the User model
class UserManager(BaseUserManager):
    # Method to create a new user instance
    def create_user(self, username, password=None, **extra_fields):
        # Check if a username is provided
        if not username:
            raise ValueError('The Username field must be set')
        # Create a new user instance
        user = self.model(username=username, **extra_fields)
        # Set the password for the user
        user.set_password(password)
        # Save the user instance
        user.save()
        # Return the user instance
        return user

    # Method to create a new superuser instance
    def create_superuser(self, username, password=None, **extra_fields):
        # Set the is_staff and is_superuser status to True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Create a new user instance with the given parameters
        return self.create_user(username, password, **extra_fields)

# Define the User model
class User(AbstractBaseUser, PermissionsMixin):
    # Define fields for the User model
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, related_name='myapp_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='myapp_user_permissions', blank=True)

    # Set the custom manager for the User model
    objects = UserManager()

    # Define the username and email fields as required
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    # Define a string representation of the User model
    def __str__(self):
        return self.username

    # Define methods to get the full and short names of the User model
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

# Define the Course model
class Course(models.Model):
    # Define fields for the Course model
    id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=200)
    Sections = models.ManyToManyField('Section', blank=True)

# Define the Section model
class Section(models.Model):
    # Define a field for the Section model
    name=models.CharField(max_length=150)

# Add the Instructor model
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # other fields as needed

# Update the Course model to include a ForeignKey to the Instructor model
class Course(models.Model):
    # existing fields
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
