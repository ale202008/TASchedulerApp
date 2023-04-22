from django.test import TestCase, Client
from TASchedulerWebApp.models import *

class LoginTestCases(TestCase):
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
            self.AssertTrue(User.objects.filter(username = i).exists(), msg = "Username does not exist in the database despite user creation.")
