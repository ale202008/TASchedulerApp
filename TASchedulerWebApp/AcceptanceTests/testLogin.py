from django.test import TestCase, Client
from TASchedulerWebApp.models import *
from django.shortcuts import reverse
from TASchedulerWebApp.views import Login

class NewUserCreationLoginTestCase(TestCase):
    def setUp(self):
        # Setups a Client user to navigate through functions/site.
        self.UserClient = Client()
        self.UserList = {"one"}

        # Similar to our TestSessionLab2Assignment, makes a username and password bases off the item
        # in the list, saves it into the database and sends it to the post method of Login to get
        # back information to validate.
        for i in self.UserList:
            tempUser = User.objects.create(username = i, password = i)
            tempUser.save()
            self.UserClient.post("/", {"username": i, "password": i}, follow = True)

    def test_LoginUsernameExists(self):
        # Checks to see after creating an account via POST that the username of the account exists within the database.
        for i in self.UserList:
            self.assertTrue(User.objects.filter(username = i).exists(), msg = "Username does not exist in the database despite user creation.")

    def test_LoginPasswordExists(self):
        # Checks to see after creating an account via POST that the password of the account exists within the database.
        for i in self.UserList:
            self.assertTrue(User.objects.filter(password = i).exists(), msg = "Password does not exist in the database despite user creation.")

    def test_LoginUserCorrectUsername(self):
        # Checks to see after user creation that the username field is the one that was inputted.
        for i in self.UserList:
            self.assertEqual(User.objects.first().username, i, msg = "Username field is incorrect after user creation.")

    def test_LoginUserCorrectPassword(self):
        # Checks to see after user creation that the password field is the one that was inputted.
        for i in self.UserList:
            self.assertEqual(User.objects.first().password, i, msg = "Password field is incorrect after user creation.")


class SuccessfulSuperUserLogin(TestCase):
    def setUp(self):
        # Setups a Client user to navigate through functions/site.
        self.UserClient = Client()
        self.UserList = {"one"}

        # Similar to our TestSessionLab2Assignment, makes a username and password bases off the item
        # in the list, saves it into the database and sends it to the post method of Login to get
        # back information to validate.
        for i in self.UserList:
            tempUser = User.objects.create(username=i, password=i)
            tempUser.save()
            self.UserClient.post("/", {"username": i, "password": i}, follow=True)

    def test_SuccesfulLogin(self):
        # Checks that with an existing user account that upon a successful login the login page is
        # redirected to the directory page. Maybe fixed?
        for i in self.UserList:
            resp = self.UserClient.post('/', {'username': i, 'password': i})
            self.assertEqual(resp.status_code, 302)



    # def test_CorrectDisplay(self):
    #     for i in self.UserList:
    #         resp = self.UserClient.post("/", {'username': i, 'password': i}, follow=True)
    #         buttons = [
    #             ('Courses', 'CoursePage/'),
    #             ('Account Info', '/account'),
    #             ('Notifications', '/notifications'),
    #             ('Sections', '/sections'),
    #             ('TAs', '/tas'),
    #             ('Instructors', '/instructors'),
    #             ('Create Course', 'AddCoursePage/'),
    #             ('Create Section', '/create_section'),
    #             ('Create Account', '/create_account'),
    #         ]
    #         self.assertEqual(resp['options'], buttons, msg = "no")