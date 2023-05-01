from django.test import TestCase, Client
from TASchedulerWebApp.models import *

class AssignSection(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.User = User.objects.create(username='Taylor@gmail.com', password='Swift')
        self.User.save()
        self.Course = Course.objects.create(name="Course", id= 000, Instructor=self.User)
        self.Course.save()
        self.Section = Section.objects.create(id=100, Course = self.Course)

    def test_AssignTA(self):
        resp = self.UserClient.post('/AssignSection/', {'teacher_assistant': self.User})
        self.assertEqual(resp.context['message'], "Teacher Assistant was assigned!", msg = "no msg was given.")
        self.assertContains(Section, self.User, msg_prefix = "Section does not contain TA")

    def test_AssignInstructor(self):
        resp = self.UserClient.post('/AssignSection/', {'instructor': self.User})
        self.assertEqual(resp.context['message'], "Instructor was assigned!", msg = "no msg was given.")
        self.assertContains(Section, self.User, msg_prefix = "Section does not contain Instructor")

    def test_Blank(self):
        resp = self.UserClient.post('/AssignSection/', {'instructor': ""})
        self.assertEqual(resp.context['message'], "Please enter an Instructor or Teacher Assistant", msg = "no msg was given.")

