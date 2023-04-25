from django.test import TestCase, Client
from TASchedulerWebApp.models import *

class AddSectionTestCase(TestCase):
    def setUp(self):
            self.UserClient = Client()
            self.User = User.objects.create(username='Taylor', password='Swift')
            self.User.save()
            self.Course = Course.objects.create(name = "COMPSCI", id = "361")
            self.Course.save()
            self.SectionName = "Section"

    def test_SectionCreation(self):
        # Hasn't been implemented yet.
        resp = self.UserClient.post("/SectionPage/", {'name': self.SectionName, 'Course': self.Course, 'TA': self.User})
        list_Sections = list(Section.objects.all())
        self.assertEqual(resp.context['Sections'], list_Sections, msg = "Section doesn't exist within the database despite being added.")

    def test_NoNameSection(self):
        # Hasn't been implemented yet.
        resp = self.UserClient.post('/AddSection/', {'name': "", 'Course': self.Course, 'TA': self.User})
        self.assertEqual(resp.context['message'], "section not created.", msg = "Section name was not provided, but still processed.")

    def test_NoCourseSection(self):
        # Hasn't been implemented yet.
        resp = self.UserClient.post('/AddSection/', {'name': self.SectionName, 'Course': "", 'TA': self.User})
        self.assertEqual(resp.context['message'], "section not created.", msg = "Course name was not provided, but still processed.")

    def test_NoTACourse(self):
        # Hasn't been implemented yet.
        resp = self.UserClient.post('/AddSection/', {'name': self.SectionName, 'Course': self.Course, 'TA': ''})
        self.assertEqual(resp.context['message'], "section not created.", msg = "TA was not provided, but still processed.")
