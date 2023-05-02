from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from TASchedulerWebApp.models import *

class AccountDeletionTestCase(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
           email='admin@example.com', password='adminpassword'
        )

        # Create a test user to be deleted
        self.test_user = User.objects.create_user(
            email='testuser@example.com', password='testpassword'
        )

    def test_delete_account(self):
        # Log in with the admin user
        self.client.login(email='admin@example.com', password='adminpassword')

        # Define the URL for the account_creation view
        account_creation_url = reverse('account_creation')  # Replace 'account_creation' with the correct URL pattern name

        # Prepare the form data to delete the test user
        form_data = {
            'emailSelect': self.test_user.pk,
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': False,
            'delete_account': True,
        }

        # Send a POST request to the account_creation view
        response = self.client.post(account_creation_url, data=form_data)

        # Check that the test user was deleted from the database
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email='testuser@example.com')

