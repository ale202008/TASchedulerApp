from django.test import TestCase, Client
from TASchedulerWebApp.models import *

class AssignSection(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.User = User.objects.create(email='Taylor@gmail.com', password='Swift', first_name = 'Taylor')
        self.User.save()
        self.Course = Course.objects.create(name="Course", id= 000, Instructor=self.User)
        self.Course.save()
        self.Section = Section.objects.create(id=100, Course = self.Course)

    def test_AssignTA(self):
        resp = self.UserClient.post('/AssignSection/', {'chosen': 'Assign','select_section': self.Section.id, 'select_teacher_assistant': self.User.first_name, 'select_instructor': ''})
        section = resp.context['section_saved']
        self.assertTrue(section.TeacherAssistant == self.User, msg = "Teacher Assistant is not correct. ")

    def test_AssignInstructor(self):
        resp = self.UserClient.post('/AssignSection/', {'chosen': 'Assign','select_section': self.Section.id, 'select_teacher_assistant': '', 'select_instructor': self.User.first_name})
        section = resp.context['section_saved']
        self.assertTrue(section.Instructor == self.User, msg = "Instructor is not correct. ")

    def test_TABlank(self):
        resp = self.UserClient.post('/AssignSection/', {'chosen': 'Assign','select_section': self.Section.id, 'select_teacher_assistant': '', 'select_instructor': self.User.first_name})
        context = 'Assign successful for section: 100'
        self.assertEqual(resp.context['message2'], context, msg = "no msg was given.")

    def test_InstructorBlank(self):
        resp = self.UserClient.post('/AssignSection/', {'chosen': 'Assign','select_section': self.Section.id, 'select_teacher_assistant': self.User.first_name, 'select_instructor': ''})
        context = 'Assign successful for section: 100'
        self.assertEqual(resp.context['message2'], context, msg = "no msg was given.")

    def test_AllBlank(self):
        resp = self.UserClient.post('/AssignSection/', {'chosen': 'Assign','select_section': self.Section.id, 'select_teacher_assistant': '', 'select_instructor': ''})
        context = 'Assign successful for section: 100'
        self.assertEqual(resp.context['message2'], context, msg = "no msg was given.")