from django.test import TestCase, Client
from TASchedulerWebApp.models import *

class AddCourseTestCases(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.User = User.objects.create(email='Taylor@gmail.com', password='Swift')
        self.Course1_name = "one"
        self.Course1_id = 1
        self.User.save()

    def test_CourseCreation(self):
        # Will check if user has the courses added to themselves
        # Also inherently checks if everything is same, fields, elements, all that stuff
        resp = self.UserClient.post('/AddCoursePage/', {'CourseName': self.Course1_name, 'CourseNumber': self.Course1_id})
        self.assertTrue(Course.objects.filter(name = self.Course1_name, id = self.Course1_id).exists(), msg = "Course doesn't exist within the database despite being added.")

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
    # Need AcceptanceTests to reflect Instructor field, ManyToManyField for courses for users.
class DeleteCourseTestCases(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.User = User.objects.create(email='Taylor@gmail.com', password='Swift')
        self.User.save()
        self.Course = Course.objects.create(id = 361, name = "Course")
        self.Course.save()

    def test_CheckDeletion(self):
        # Checks to see if course is deleted through post method given a Course Number
        resp = self.UserClient.post('/DeleteCoursePage/', {'CourseNumber': 361})
        list_Courses = list(Course.objects.all())
        self.assertEqual(resp.context['Courses'], list_Courses, msg="Course doesn't exist within the database despite being added.")

    def test_InvalidCourseField(self):
        # Checks to see if an error/exception is given when a Course is attempted to be deleted, but does not exist.
        # this should fail as it is not possible to try to delete invalid course numbers due to drop down bar
        resp = self.UserClient.post('/DeleteCoursePage/', {'CourseNumber': 11111111111})
        self.assertRedirects(resp, '/CoursePage/', msg_prefix = "Course was not in the database, but was deleted. How?")

    def test_BlankCourseField(self):
        # Checks to see if an error/exception is given when a Course field is blank.
        resp = self.UserClient.post('/DeleteCoursePage/', {'CourseNumber': ""})
        self.assertEqual(resp.context['message'], "Please choose a course", msg = "Course was not in the database, but was deleted. How?")