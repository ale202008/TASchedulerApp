from django.test import TestCase
from TASchedulerWebApp.models import *
from TASchedulerWebApp.views import *

class AssignSectionTestCase(TestCase):
    def setUp(self):
        self.Instructor = User.objects.create(email = "instructor@email.com", password = 'instructor', is_staff = True)
        self.Instructor.save()
        self.TA = User.objects.create(email = "ta@email.com", password = 'ta', is_staff = False)
        self.TA.save()
        self.Course = Course.objects.create(id = 361, name = 'COMPSCI', Instructor=self.Instructor, TeacherAssistant=self.TA)
        self.Course.save()
        self.Section = Section.objects.create(id = 100, Course = self.Course)
        self.Section.save()

    def test_setInstructorNone(self):
        test = AssignSection.set_instructor(self, '')
        self.assertEqual(test, None, msg = 'Not none.')

    def test_setInstructor(self):
        test = AssignSection.set_instructor(self, self.Instructor.email)
        self.assertEqual(test, self.Instructor, msg = 'Instructor was not retrieved')

    def test_setTANone(self):
        test = AssignSection.set_instructor(self, '')
        self.assertEqual(test, None, msg = 'Not none.')

    def test_setTA(self):
        test = AssignSection.set_teacher_assistant(self, self.TA.email)
        self.assertEqual(test, self.TA, msg = 'TA was not retrieved')

    def test_getCourses(self):
        test = AssignSection.get_courses(self)
        self.assertEqual(list(Course.objects.all()), test, msg = 'Not Equal')

    def test_getCourseSection(self):
        test = AssignSection.get_course_sections(self, self.Course)
        self.assertEqual(list(Section.objects.filter(Course = self.Course)), test, msg = 'Not Equal')

    def test_getCourseInstructors(self):
        test = AssignSection.get_teacher_assistants(self)
        self.assertEqual(list(User.objects.filter(is_superuser=False, is_staff=False)), test, msg = 'Not Equal')

    def test_getTAs(self):
        test = AssignSection.get_courses(self)
        self.assertEqual(list(Course.objects.all()), test, msg = 'Not Equal')