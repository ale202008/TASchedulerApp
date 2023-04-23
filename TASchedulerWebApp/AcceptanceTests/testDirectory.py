from django.test import TestCase, Client
from TASchedulerWebApp.models import *
from django.urls import reverse

#Will Probably split class in Three for each separate user and narrow down test cases.
class DirectorySuperUserRedirectTestCases(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.User = User.objects.create(username = "Taylor", password = "Swift", is_superuser=True)
        self.User.save()
        self.directory_url = reverse('directory')
        # Forces the login for the given user, pretty useful.
        self.UserClient.force_login(self.User)
        # Gets the information that is presented by the Directory function given a user
        # is logged in. In this case it is through the Client().
        self.resp = self.UserClient.get(self.directory_url)

    def test_SuperUserCourseRedirect(self):
        self.assertContains(self.resp, 'Courses', msg_prefix="Course is not displayed")
    def test_SuperUserAccountInfoRedirect(self):
        self.assertContains(self.resp, 'Account Info', msg_prefix="Account Info is not displayed")
    def test_SuperUserNotificationsRedirect(self):
        self.assertContains(self.resp, 'Notifications', msg_prefix="Notifications is not displayed")
    def test_SuperUserSectionsRedirect(self):
        self.assertContains(self.resp, 'Sections', msg_prefix="Sections is not displayed")
    def test_SuperUserTARedirect(self):
        self.assertContains(self.resp, 'TAs', msg_prefix="TA is not displayed")
    def test_SuperUserInstructorsRedirect(self):
        self.assertContains(self.resp, 'Instructors', msg_prefix="Instructors is not displayed")
    def test_SuperUserCreateCourseRedirect(self):
        self.assertContains(self.resp, 'Create Course', msg_prefix="Create Course is not displayed")
    def test_SuperUserCreateSectionRedirect(self):
        self.assertContains(self.resp, 'Create Section', msg_prefix="Create Section is not displayed")
    def test_SuperUserCreateAccountRedirect(self):
        self.assertContains(self.resp, 'Create Account', msg_prefix="Create Account not displayed")

class DirectoryInstructorRedirectsTestCases(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.User = User.objects.create(username="Taylor", password="Swift", is_staff=True)
        self.User.save()
        self.directory_url = reverse('directory')
        self.UserClient.force_login(self.User)
        self.resp = self.UserClient.get(self.directory_url)

    def test_InstructorCourseRedirect(self):
        self.assertContains(self.resp, 'Courses', msg_prefix="Course is not displayed")
    def test_InstructorAccountInfoRedirect(self):
        self.assertContains(self.resp, 'Account Info', msg_prefix="Account Info is not displayed")
    def test_InstructorNotificationsRedirect(self):
        self.assertContains(self.resp, 'Notifications', msg_prefix="Notifications is not displayed")
    def test_InstructorSectionsRedirect(self):
        self.assertContains(self.resp, 'Sections', msg_prefix="Sections is not displayed")
    def test_InstructorTARedirect(self):
        self.assertContains(self.resp, 'TAs', msg_prefix="TA is not displayed")
    def test_InstructorInstructorsRedirect(self):
        self.assertNotContains(self.resp, 'Instructors', msg_prefix="Instructors is displayed")
    def test_InstructorCreateCourseRedirect(self):
        self.assertNotContains(self.resp, 'Create Course', msg_prefix="Create Course is displayed")
    def test_InstructorCreateSectionRedirect(self):
        self.assertNotContains(self.resp, 'Create Section', msg_prefix="Create Section is displayed")
    def test_InstructorCreateAccountRedirect(self):
        self.assertNotContains(self.resp, 'Create Account', msg_prefix="Create Account is displayed")

class DirectoryTARedirectsTestCases(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.User = User.objects.create(username="Taylor", password="Swift")
        self.User.save()
        self.directory_url = reverse('directory')
        self.UserClient.force_login(self.User)
        self.resp = self.UserClient.get(self.directory_url)

    def test_InstructorCourseRedirect(self):
        self.assertContains(self.resp, 'Courses', msg_prefix="Course is not displayed")
    def test_InstructorAccountInfoRedirect(self):
        self.assertContains(self.resp, 'Account Info', msg_prefix="Account Info is not displayed")
    def test_InstructorNotificationsRedirect(self):
        self.assertContains(self.resp, 'Notifications', msg_prefix="Notifications is not displayed")
    def test_InstructorSectionsRedirect(self):
        self.assertContains(self.resp, 'Sections', msg_prefix="Sections is not displayed")
    def test_InstructorTARedirect(self):
        self.assertContains(self.resp, 'TAs', msg_prefix="TA is not displayed")
    def test_InstructorInstructorsRedirect(self):
        self.assertNotContains(self.resp, 'Instructors', msg_prefix="Instructors is displayed")
    def test_InstructorCreateCourseRedirect(self):
        self.assertNotContains(self.resp, 'Create Course', msg_prefix="Create Course is displayed")
    def test_InstructorCreateSectionRedirect(self):
        self.assertNotContains(self.resp, 'Create Section', msg_prefix="Create Section is displayed")
    def test_InstructorCreateAccountRedirect(self):
        self.assertNotContains(self.resp, 'Create Account', msg_prefix="Create Account is displayed")



