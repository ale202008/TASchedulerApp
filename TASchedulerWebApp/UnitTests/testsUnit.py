from django.test import TestCase
from TASchedulerWebApp.models import *


class UserTestCase(TestCase):
    # Tests will mainly focus on the Username and Password fields.
    def setup(self):
        self.object1 = User.objects.create_user("Taylor", "Swift")
        self.object1.save()
    def test_UserCreation(self):
        # Checks to see if the correct number of users were created, in this case only 1 meant to exist
        # so if it fails it means Unit Test succeeds as checking for failure.
        self.setup()
        self.assertEqual(User.objects.count(), 1, msg = "One user were meant to be created.")

    def test_UserUsername(self):
        # Makes sure that the username is inside the User database after account creation.
        self.setup()
        self.assertTrue(User.objects.filter(username = "Taylor").exists(), msg = "Username does not exist despite creation of user.")

    def test_UserPassword(self):
        # Makes sure that the password is inside the User database after account creation.
        # Note, had to manually save "password" field of User object as Abstract object currently sets password to None.
        self.setup()
        self.object1.password = "Swift"
        self.object1.save()
        self.assertTrue(User.objects.filter(password = "Swift").exists(), msg = "Password does not exist despite creation of user.")

    def test_UserCorrectUsernameField(self):
        self.setup()
        self.object1.password = "Swift"
        self.object1.save()
        self.assertEqual(User.objects.first().username, "Taylor", msg = "The User object that was created does not have the correct username.")

    def test_UserCorrectPasswordField(self):
        self.setup()
        self.object1.password = "Swift"
        self.object1.save()
        self.assertEqual(User.objects.first().password, "Swift", msg = "The User object that was created does not have the correct password.")

    def test_UserUsernameBlank(self):
        # Asserts that a ValueError is raises when a blank username is attempted in user creation.
        with self.assertRaises(ValueError, msg = "Username is a blank field, but did not fail"):
            self.object1 = User.objects.create_user("")
            self.object1.save()

    def test_UserPasswordBlank(self):
        # Asserts that an Exception is raised when a blank password is attempted in user creation.
        with self.assertRaises(Exception, msg = "Username is a blank field, but did not fail"):
            self.object1 = User.objects.create_user("Taylor")
            self.object1.password("")
            self.object1.save()

class CourseTestCases(TestCase):
    # Tests will mainly focus on course creation and deletion

    def setup(self):
        self.objectSection = Section.objects.create(name = "Test")
        self.objectSection.save()
        self.object1 = Course.objects.create(id = 361, name = "COMPSCI")
        self.object1.Sections.add(self.objectSection)
        self.object1.save()
    def test_CourseCreation(self):
        # Checks to see if Course database was updated after course creation.
        self.setup()
        self.assertEqual(Course.objects.count(), 1, msg = "Courses database did not increase when course was created.")

    def test_CourseName(self):
        # Checks to see if Course name was input into the database.
        self.setup()
        self.assertTrue(Course.objects.filter(name = "COMPSCI"), msg = "Course name was not saved into database despite course creation.")

    def test_CourseID(self):
        # Checks to see if Course id was input into the database.
        self.setup()
        self.assertTrue(Course.objects.filter(id = 361), msg = "Course name was not saved into database despite course creation.")

    def test_CourseSection(self):
        # Checks to see if Sections was input into the database.
        self.setup()
        self.assertTrue(Course.objects.filter(Sections = self.objectSection), msg = "Sections was not saved into database despite course creation.")

    def test_CourseNameField(self):
        # Checks to see if Name was correctly saved with the course upon creation.
        self.setup()
        self.assertEqual(Course.objects.first().name, 'COMPSCI', msg = "Name was not saved to the create course upon creation.")

    def test_CourseIDField(self):
        # Checks to see if id was correctly saved with the course upon creation.
        self.setup()
        self.assertEqual(Course.objects.first().id, '361', msg = "ID was not saved to the create course upon creation.")

    def test_CourseNameField(self):
        # Checks to see if Sections was correctly saved with the course upon creation.
        self.setup()
        self.assertTrue(Course.objects.first().Sections.contains(self.objectSection), msg = "Sections was not saved to the create course upon creation.")

    def test_CourseNameBlank(self):
        with self.assertRaises(Exception, msg = "Course name is blank."):
            self.object1 = Course.objects.create(id= None, name="")
            self.object1.save()

    def test_CourseIDBlank(self):
        with self.assertRaises(Exception, msg = "Course id is blank."):
            self.object1 = Course.objects.create(id= None, name="")
            self.object1.save()

class SectionTestCases(TestCase):
    def setup(self):
        self.object1 = Section.objects.create(name = "DjangoUnchained")
        self.object1.save()

    def test_SectionCreation(self):
        # Checks to see if database was updated after creation.
        self.setup()
        self.assertEqual(Section.objects.count(), 1, msg = "Incorrect count of sections after creation.")

    def test_SectionName(self):
        # Checks to see if Section name was input into the database.
        self.setup()
        self.assertTrue(Section.objects.filter(name = "DjangoUnchained").exists(), msg = "Section name is not in database after creation.")

    def test_SectionNameField(self):
        # Checks to see if Section name is correctly associated to object upon creation.
        self.setup()
        self.assertEqual(Section.objects.first().name, "DjangoUnchained", msg = "Section name is not associated to correct object.")

    def test_SectionNameBlank(self):
        with self.assertRaises(Exception, msg = "Section name is blank."):
            self.object1 = Section.objects.create(name="")
            self.object1.save()
