from django.test import TestCase
from TASchedulerWebApp.models import *


class UserTestCase(TestCase):
    def test_UserCreation(self):
        # Checks to see if the correct number of users were created, in this case only 1 meant to exist
        # so if it fails it means Unit Test succeeds as checking for failure.
        self.object1 = User.objects.create_user("Taylor", "Swift")
        self.object1.save()
        self.assertEqual(User.objects.count(), 1, msg = "One user were meant to be created.")
    def test_UserUsername(self):
        # Makes sure that the username is inside the User database after account creation.
        self.object1 = User.objects.create_user("Taylor", "Swift")
        self.object1.save()
        self.assertTrue(User.objects.filter(username = "Taylor").exists(), msg = "Username does not exist despite creation of user.")
    def test_UserPassword(self):
        # Makes sure that the password is inside the User database after account creation.
        # Note, had to manually save "password" field of User object as Abstract object currently sets password to None.
        self.object1 = User.objects.create_user("Taylor", "Swift")
        self.object1.password = "Swift"
        self.object1.save()
        self.assertTrue(User.objects.filter(password = "Swift").exists(), msg = "Password does not exist despite creation of user.")
    def test_UserCorrectUsernameField(self):
        self.object1 = User.objects.create_user("Taylor", "Swift")
        self.object1.password = "Swift"
        self.object1.save()
        self.assertEqual(User.objects.first().username, "Taylor", msg = "The User object that was created does not have the correct username.")
    def test_UserCorrectPasswordField(self):
        self.object1 = User.objects.create_user("Taylor", "Swift")
        self.object1.password = "Swift"
        self.object1.save()
        self.assertEqual(User.objects.first().password, "Swift", msg = "The User object that was created does not have the correct password.")







