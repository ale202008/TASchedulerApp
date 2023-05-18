from django.test import TestCase, Client
from TASchedulerWebApp.models import *

class testNotification(TestCase):
    def setUp(self):
        self.notification = 'test'
        self.client = Client()
        self.TestUser = User.objects.create(email='test@gmail.com', password='test')
        self.TestUser.save()
        self.ReceiveUser = User.objects.create(email='send@gmail.com', password='send')

    def testSend(self):
        context = {'chosen': 'Send Message', 'select_user': self.ReceiveUser.email, 'new_notification': self.notification}
        resp = self.client.post('/Notification/', context)
        self.assertEqual(resp.context['message'], 'Notification sent!', msg = 'Notification not sent.')