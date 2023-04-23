from django.test import TestCase, Client
from TASchedulerWebApp.models import *
from django.urls import reverse

#Will Probably split class in Three for each separate user and narrow down test cases.
class DirectorySuperUserRedirectTestCases(TestCase):
    def setUp(self):
        self.UserClient = Client()
        self.User = User.objects.create(username = "Taylor", password = "Swift")
        self.User.save()
        self.directory_url = reverse('directory')

    def test_CorrectSuperUserDisplay(self):
        # Checks that given the exising user account is of SuperUser status that it properly
        # displays the form that is built by the function Directory as options is equal to the
        # buttons displayed. Maybe a unit test rather than an acceptance test.
        self.User.is_superuser = True
        self.User.save()
        # Forces the login for the given user, pretty useful.
        self.UserClient.force_login(self.User)
        # Gets the information that is presented by the Directory function given a user
        # is logged in. In this case it is through the Client().
        resp = self.UserClient.get(self.directory_url)

        self.assertContains(resp, 'Courses', msg_prefix="Course is not displayed")
        self.assertContains(resp, 'Account Info', msg_prefix="Account Info is not displayed")
        self.assertContains(resp, 'Notifications', msg_prefix="Notifications is not displayed")
        self.assertContains(resp, 'Sections', msg_prefix="Sections is not displayed")
        self.assertContains(resp, 'TAs', msg_prefix="TA is not displayed")
        self.assertContains(resp, 'Instructors', msg_prefix="Instructors is not displayed")
        self.assertContains(resp, 'Create Course', msg_prefix="Create Course is not displayed")
        self.assertContains(resp, 'Create Section', msg_prefix="Create Section is not displayed")
        self.assertContains(resp, 'Create Account', msg_prefix="Create Account not displayed")

    def test_CorrectInstructorDisplay(self):
        # Similar to the previous test for SuperUser, except we also check that the form
        # does not contain any unpermitted buttons.
        self.User.is_staff = True
        self.User.save()
        self.UserClient.force_login(self.User)
        resp = self.UserClient.get(self.directory_url)

        self.assertContains(resp, 'Courses', msg_prefix="Course is not displayed")
        self.assertContains(resp, 'Account Info', msg_prefix="Account Info is not displayed")
        self.assertContains(resp, 'Notifications', msg_prefix="Notifications is not displayed")
        self.assertContains(resp, 'Sections', msg_prefix="Sections is not displayed")
        self.assertContains(resp, 'TAs', msg_prefix="TA is not displayed")
        self.assertNotContains(resp, 'Instructors', msg_prefix="Instructors is displayed")
        self.assertNotContains(resp, 'Create Course', msg_prefix="Create Course is displayed")
        self.assertNotContains(resp, 'Create Section', msg_prefix="Create Section is displayed")
        self.assertNotContains(resp, 'Create Account', msg_prefix="Create Account is displayed")

    def test_CorrectTADisplay(self):
        # Same as the previous code
        self.UserClient.force_login(self.User)
        resp = self.UserClient.get(self.directory_url)

        self.assertContains(resp, 'Courses', msg_prefix="Course is not displayed")
        self.assertContains(resp, 'Account Info', msg_prefix="Account Info is not displayed")
        self.assertContains(resp, 'Notifications', msg_prefix="Notifications is not displayed")
        self.assertContains(resp, 'Sections', msg_prefix="Sections is not displayed")
        self.assertContains(resp, 'TAs', msg_prefix="TA is not displayed")
        self.assertNotContains(resp, 'Instructors', msg_prefix="Instructors is isplayed")
        self.assertNotContains(resp, 'Create Course', msg_prefix="Create Course is displayed")
        self.assertNotContains(resp, 'Create Section', msg_prefix="Create Section is displayed")
        self.assertNotContains(resp, 'Create Account', msg_prefix="Create Account is displayed")
