from django.test import TestCase, Client
from TASchedulerWebApp.models import User
from django.urls import reverse


class CreateAccountTestCases(TestCase):
    def setUp(self):

        self.admin_user = User.objects.create_superuser(
            email='admin@example.com', password='adminpassword'
        )
        # Create a test user to be deleted
        self.test_staff_user = User.objects.create_user(
            email='staffuser@example.com', password='testpassword', is_staff='True', first_name='lookatme'
        )
        self.test_ta_user = User.objects.create_user(
            email='tauser@example.com', password='testpassword', is_staff='False'
        )
        self.email = "test@test.com"
        self.first_name = "testfirst"
        self.last_name = "testlast"
        self.password = "test"
        self.password_confirm = "test"

    def test_AccountCreateInstructor(self):
        self.client.login(email='admin@example.com', password='adminpassword')

        account_creation_url = reverse('account_creation')

        # Test Instructor Account Creation
        form = {'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'is_staff': 'False',
                'password': self.password,
                'password_confirm': self.password_confirm,
                'create': '',
                'submit': '',
        }

        response = self.client.post(account_creation_url, data=form)
        if response.status_code == 200:
            try:
                list_users = User.objects.get(email=self.email)
            except FileNotFoundError:
                self.assertRaises(FileNotFoundError, msg='No User Found in the Data Base')
            self.assertEqual(self.email, list_users.email,
                             msg="User doesn't exist within the database despite being added.")
        else:
            self.assertRaises(FileNotFoundError, msg='HTTP Did Not Respond with 200')
        self.client.login(email='admin@example.com', password='adminpassword')


    def test_AccountCreateTA(self):
        self.client.login(email='admin@example.com', password='adminpassword')

        account_creation_url = reverse('account_creation')

        # Test Instructor Account Creation
        form = {'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'is_staff': 'False',
                'password': self.password,
                'password_confirm': self.password_confirm,
                'create': '',
                'submit': '',
                }
        response = self.client.post(account_creation_url, data=form)
        if response.status_code == 200:
            try:
                list_users = User.objects.get(email=self.email)
            except FileNotFoundError:
                self.assertRaises(FileNotFoundError, msg='No User Found in the Data Base')
            self.assertEqual(self.email, list_users.email,
                             msg="User doesn't exist within the database despite being added.")
        else:
            self.assertRaises(FileNotFoundError, msg='HTTP Did Not Respond with 200')

    def test_AccountCreateBadEmail(self):
        self.client.login(email='admin@example.com', password='adminpassword')

        account_creation_url = reverse('account_creation')

        # Test Instructor Account Creation
        form = {'email': 'admin@example.com',
                'first_name': self.first_name,
                'last_name': self.last_name,
                'is_staff': 'False',
                'password': self.password,
                'password_confirm': self.password_confirm,
                'create': '',
                'submit': '',
                }
        response = self.client.post(account_creation_url, data=form)
        if response.status_code == 200:
            list_users = list(User.objects.filter(email=self.email))
            self.assertEqual(len(list_users), 0, msg='No User Found in the Data Base')
        else:
            self.assertRaises(FileNotFoundError, msg='HTTP Did Not Respond with 200')

    def test_AccountCreateDifferentPass(self):
        self.client.login(email='admin@example.com', password='adminpassword')

        account_creation_url = reverse('account_creation')

        # Test Instructor Account Creation
        form = {'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'is_staff': 'False',
                'password': self.password,
                'password_confirm': 'testfail',
                'create': '',
                'submit': '',
                }
        response = self.client.post(account_creation_url, data=form)
        if response.status_code == 200:
            list_users = list(User.objects.filter(email=self.email))
            self.assertEqual(len(list_users), 0, msg='No User Found in the Data Base')
        else:
            self.assertRaises(FileNotFoundError, msg='HTTP Did Not Respond with 200')

    def test_AccountCreateNoFirst(self):
        self.client.login(email='admin@example.com', password='adminpassword')

        account_creation_url = reverse('account_creation')

        # Test Instructor Account Creation
        form = {'email': self.email,
                'first_name': '',
                'last_name': self.last_name,
                'is_staff': 'False',
                'password': self.password,
                'password_confirm': self.password_confirm,
                'create': '',
                'submit': '',
                }
        response = self.client.post(account_creation_url, data=form)
        if response.status_code == 200:
            list_users = list(User.objects.filter(email=self.email))
            self.assertEqual(len(list_users), 0, msg='No User Found in the Data Base')
        else:
            self.assertRaises(FileNotFoundError, msg='HTTP Did Not Respond with 200')


    def test_AccountEditMakeStaff(self):
        self.client.login(email='admin@example.com', password='adminpassword')

        account_creation_url = reverse('account_creation')

        # Test Instructor Account Creation
        form = {'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'is_staff': 'True',
                'emailSelect': 10,
                'edit': '',
                'submit': '',
                }
        response = self.client.post(account_creation_url, data=form)
        if response.status_code == 200:
            list_users = list(User.objects.filter(email='tauser@example.com'))
            self.assertEqual(len(list_users), 0, msg='Email not changed found in the Data Base')
        else:
            self.assertRaises(FileNotFoundError, msg='HTTP Did Not Respond with 200')

    def test_AccountEditTA(self):
        self.client.login(email='admin@example.com', password='adminpassword')

        account_creation_url = reverse('account_creation')

        # Test Instructor Account Creation
        form = {'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'is_staff': 'False',
                'emailSelect': 10,
                'edit': '',
                'submit': '',
                }
        response = self.client.post(account_creation_url, data=form)
        if response.status_code == 200:
            list_users = list(User.objects.filter(email='tauser@example.com'))
            self.assertEqual(len(list_users), 0, msg='Email not changed found in the Data Base')
        else:
            self.assertRaises(FileNotFoundError, msg='HTTP Did Not Respond with 200')
