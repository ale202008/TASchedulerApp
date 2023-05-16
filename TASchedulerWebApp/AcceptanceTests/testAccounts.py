from django.test import TestCase, Client
from TASchedulerWebApp.models import User


class CreateAccountTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "test@test.com"
        self.first_name = "test"
        self.last_name = "testlast"
        self.password = "test"
        self.password_confirm = "test"

    def test_AccountCreation(self):
        # Test Instructor Account Creation
        form = {'username': self.username, 'first_name': self.first_name, 'last_name': self.last_name,
                'is_staff': 'on', 'password': self.password, 'password_confirm':self.password_confirm, 'submit': ''}
        resp = self.client.post('account_creation/', {'form': form})
        print(resp)
        list_users = list(User.objects.all())
        # if resp.POST['username']
        self.assertEqual(resp.context['username'], list_users,
                         msg="User doesn't exist within the database despite being added.")

    def test_AccountEdit(self):
        # Test Account Edit
        form = {'username': self.username, 'first_name': self.first_name, 'last_name': self.last_name,
                'is_staff': 'on', 'submit': ''}
        resp = self.client.post('account_creation/', {'form': form})
        print(resp)
        list_users = list(User.objects.all())
        # if resp.POST['username']
        self.assertEqual(resp.context['username'], list_users,
                         msg="User doesn't exist within the database despite being added.")