from django.test import TestCase, Client
from TASchedulerWebApp.models import *


class AddSectionTestCase(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.Course = Course.objects.create(name="COMPSCI", id="361")
        self.Course.save()
        self.SectionName = "Section"

    def test_SectionCreation(self):
        resp = self.UserClient.post('/AddSectionPage/', {'SectionNumber': "200", "create section": "361"})
        self.assertTrue((Section.objects.all().count())==1, "Section info was enter but not created")

    def test_NoNameSection(self):
        resp = self.UserClient.post('/AddSectionPage/', {'SectionNumber': "", 'create section': "361"})
        self.assertEqual(resp.context['message1'], "Section Number blank", msg="Section name was not provided, but "
                                                                               "still processed.")

    def test_NoCourseNumber(self):
        resp = self.UserClient.post('/AddSectionPage/', {'SectionNumber': "200", 'create section': ""})
        self.assertEqual(resp.context['message1'], "Please choose a course", msg="Course name was not provided, but "
                                                                                 "still processed.")


class DeleteSectionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.Course = Course.objects.create(name="COMPSCI", id="361")
        self.Course.save()
        self.Section = Section.objects.create(id=100, Course=self.Course)
        self.Section.save()

    def test_DeleteSection(self):
        resp = self.client.post('/DeleteSectionPage/', {"chosen": "100"})
        self.assertTrue(Section.objects.all().count()==0, "Section info was enter but not deleted")

    def test_NoSectionNumber(self):
        resp = self.client.post('/DeleteSectionPage/', {"chosen":""})
        self.assertEqual(resp.context['message'], "Please choose a section", msg="Course name was not provided, but "
                                                                                 "still processed.")

class SectionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.Course1 = Course.objects.create(name="COMPSCI", id="361")
        self.Course1.save()
        self.Course2 = Course.objects.create(name="intro", id="250")
        self.Course2.save()
        self.Section1 = Section.objects.create(id=100, Course=self.Course1)
        self.Section1.save()
        self.Section2 = Section.objects.create(id=101, Course=self.Course1)
        self.Section2.save()
        self.Section3 = Section.objects.create(id=102, Course=self.Course1)
        self.Section3.save()

    def test_CourseSectionsExist(self):
        resp = self.client.post('/SectionPage/', {"show section":"361"})
        self.assertContains(resp, "100")
        self.assertContains(resp, "101")
        self.assertContains(resp, "102")

    def test_CourseNoSection(self):
        resp = self.client.post('/SectionPage/', {"show section":"250"})
        self.assertEqual(resp.context['message'], "No section for this course", msg="no course exist to be displayed")

    def test_NoCourseSelected(self):
        resp = self.client.post('/SectionPage/', {"show section": ""})
        self.assertEqual(resp.context['message'], "Please choose a course", msg="course doesn't exist to be displayed")

class AssignSessionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.Instructor = User.objects.create(email = 'instructor@gmail.com', password = 'instructor', is_staff = True)
        self.Instructor.save()
        self.TA = User.objects.create(email = 'ta@gmail.com', password = 'ta', is_staff = False)
        self.TA.save()
        self.Course = Course.objects.create(name="COMPSCI", id="361", Instructor = self.Instructor, TeacherAssistant = self.TA)
        self.Course.save()
        self.Section = Section.objects.create(id=100, Course=self.Course)
        self.Section.save()

    def test_AssignInstructor(self):
        context = {'chosen': 'Assign', 'select_section': self.Section.id, 'select_instructor': self.Instructor.email, 'select_teacher_assistant': ''}
        resp = self.client.post('/AssignSection/', context)
        self.assertEqual(resp.context['message2'], 'Assign successful for section: ' + str(self.Section.id), msg = 'Instructor was not assigned.')

    def test_AssignTA(self):
        context = {'chosen': 'Assign', 'select_section': '100', 'select_instructor': '', 'select_teacher_assistant': self.TA.email}
        resp = self.client.post('/AssignSection/', context)
        self.assertEqual(resp.context['message2'], 'Assign successful for section: ' + str(self.Section.id), msg = 'TA was not assigned.')