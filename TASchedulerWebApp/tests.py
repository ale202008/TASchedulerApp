from .models import Supervisor, Instructor, TeacherAssistant, Course, LabSection, LectureSection
from django.test import TestCase, Client

# Create your tests here.
class TestCreateCourse(TestCase):
    client = None
    def setUp(self):
        self.client = Client()


    def test_CreateCourse(self):
        response = self.client.post("AddCoursePage.html", {"Course Number":"361", "Course Name":"Software Engineering"})
        self.assertContains(response, "Course created.")

