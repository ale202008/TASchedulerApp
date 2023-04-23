from django.test import TestCase, Client
from TASchedulerWebApp.models import *
from django.urls import reverse

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

class SuccessfulUserLogin(TestCase):
    def setUp(self):
        # Setups a Client user to navigate through functions/site.
        self.UserClient = Client()
        # Essentially retrieves data from the called url name, works real well when
        # a function cannot be called due to .as_view()
        self.directory_url = reverse('directory')
        self.User = User.objects.create(username = "Taylor", password = "Swift")

    def test_SuccesfulLogin(self):
        # Checks that with an existing user account that upon a successful login the login page is
        # redirected to the directory page. Maybe fixed?
        resp = self.UserClient.post('/', {'username': self.User.username, 'password': self.User.password})
        self.assertEqual(resp.status_code, 302)


class InvalidLoginTests(TestCase):
    def setUp(self):
        # Sets up the client, a user that exists already.
        self.UserClient = Client()
        self.User = User.objects.create(username='Taylor', password='Swift')
        self.User.save()

    def test_Nonexistence(self):
        # Checks to see that if a non-existing user tries to login that they are not redirected anywhere, but the login screen.
        resp = self.UserClient.post('/', {'username': 'NotTaylor', 'password': 'NotSwift'}, follow = True)
        self.assertRedirects(resp, '/', msg_prefix = "Was not redirected back to login screen. User was not created yet.")

    def test_BadUsername(self):
        # Checks to see that if user attempts to login with a blank or bad username. In our case, we are looking at
        # simply not redirecting to another webpage. Might change to an exception assertion in Test Revision.
        resp = self.UserClient.post('/', {'username': '', 'password': 'NotSwift'}, follow = True)
        self.assertRedirects(resp, '/', msg_prefix = "Was not redirected back to login screen due to bad username.")

    def test_BadPassword(self):
        # Checks to see that if user attempts to login with a wrong password. In our case, we are looking at
        # simply not redirecting to another webpage. Might change to an exception assertion in Test Revision.
        resp = self.UserClient.post('/', {'username': 'Taylor', 'password': 'NotSwift'}, follow = True)
        self.assertRedirects(resp, '/', msg_prefix = "Was not redirected back to login screen due to bad password.")