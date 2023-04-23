from django.test import TestCase, Client
from TASchedulerWebApp.models import *

class AddCourseTestCases(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.User = User.objects.create(username='Taylor', password='Swift')
        self.Course1_name = "one"
        self.Course1_id = 1
        self.User.save()

    def test_CourseCreation(self):
        # Will check if user has the courses added to themselves
        # Also inherently checks if everything is same, fields, elements, all that stuff
        self.Instructor = User.objects.create(username = "Instrurctor" , password = "Instructor")
        resp = self.UserClient.post('/AddCoursePage/', {'CourseName': self.Course1_name, 'CourseNumber': self.Course1_id})
        listCourses = list(Course.objects.all())
        self.assertEqual(resp.context['Courses'], listCourses, msg = "Course doesn't exist within the database despite being added.")

    def test_NoNameCourse(self):
        resp = self.UserClient.post('/AddCoursePage/', {'CourseName': "", 'CourseNumber': 12})
        self.assertEqual(resp.context['message'], "course not created.", msg = "Course name was not provided, but still processed.")

    def test_NoIDCourse(self):
        resp = self.UserClient.post('/AddCoursePage/', {'CourseName': "COMPSCI", 'CourseNumber': ""})
        self.assertEqual(resp.context['message'], "course not created.", msg = "Course name was not provided, but still processed.")

    def test_NoInstructorCourse(self):
        resp = self.UserClient.post('/AddCoursePage/', {'CourseName': "", 'CourseNumber': ""})
        self.assertEqual(resp.context['message'], "course not created.", msg = "Course name was not provided, but still processed.")

    # Need test to make sure that when user enters course page, all courses for user shows up.
    # Need test to make sure that when SuperUser adds a course, course shows up for course page.
    # Need tests to reflect Instructor field, ManyToManyField for courses for users.