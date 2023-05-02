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
        resp = self.UserClient.post('/AssignSection/', {'section': self.Section, 'teacher_assistant': self.User})
        self.assertTrue(self.Section.TeacherAssistant == self.User, msg = "Teacher Assistant is not correct." + self.Section.TeacherAssistant.first_name)

    def test_AssignInstructor(self):
        resp = self.UserClient.post('/AssignSection/', {'instructor': self.User})
        self.assertEqual(resp.context['message'], "Instructor was assigned!", msg = "no msg was given.")
        self.assertContains(Section, self.User, msg_prefix = "Section does not contain Instructor")

    def test_Blank(self):
        resp = self.UserClient.post('/AssignSection/', {'instructor': ""})
        self.assertEqual(resp.context['message'], "Please enter an Instructor or Teacher Assistant", msg = "no msg was given.")

