from django.test import TestCase, Client
from TASchedulerWebApp.models import *
from django.urls import reverse

class CourseTestCases(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.User = User.objects.create(username='Taylor', password='Swift')
        self.Course1_name = "one"
        self.Course1_id = 1
        self.User.save()

    def test_CourseCreation(self):
        # Will check if user has the courses added to themselves
        # Also inherently checks if everything is same, fields, elements, all that stuff
        resp = self.UserClient.post('/AddCoursePage/', {'CourseName': self.Course1_name, 'CourseNumber': self.Course1_id})
        listCourses = list(Course.objects.all())
        self.assertEqual(resp.context['Courses'], listCourses, msg = "Course doesn't exist within the database despite being added.")

