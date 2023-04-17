from TASchedulerWebApp.models import Supervisor, Instructor, TeacherAssistant, Course, LabSection, LectureSection
from unittest import TestCase

# Create your tests here.
class TestInit(TestCase):
    def test_CreateCourse(self):
        Supervisor = Supervisor.objects.create
        course = Supervisor.createCourse(self, "CompSci-361", "Software Engineering")
        self.assertEqual(course.name, "CompSci-361")
