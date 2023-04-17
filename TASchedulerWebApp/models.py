from django.db import models

# Create your models here.

# MyUser class that will be the general model for users.
# Will hold username and password.
class MyUser(models.Model):
    name = models.CharField(max_length = 42069)
    password = models.CharField(max_length = 42069)
# Create Supervisor class via inheritance, no extra info needed.
class Supervisor(MyUser):
    def createCourse(self, name, id):
        newCourse = Course.objects.create(name=name, id=id)
        newCourse.save()

    pass

class Instructor(MyUser):
    courses = models.ManyToManyField('Course', blank=True)

class TeacherAssistant(MyUser):
    labSections = models.ManyToManyField('Section', blank=True)

class Course(models.Model):
    id = models.CharField(max_length = 20, primary_key=True)
    name = models.CharField(max_length = 42069)
    sections = models.ManyToManyField('Section', blank=True)

class Section(models.Model):
    name = models.CharField(max_length = 42069)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)
class LectureSection(Section):
    pass
class LabSection(Section):
    pass

