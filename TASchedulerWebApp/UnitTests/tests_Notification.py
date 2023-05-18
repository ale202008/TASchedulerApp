from django.test import TestCase
from TASchedulerWebApp.models import *
from TASchedulerWebApp.views import *

class NotificationTestCase(TestCase):
    def setUp(self):
        self.Instructor = User.objects.create(email = "instructor@email.com", password = 'instructor', is_staff = True)
        self.Instructor.save()
        self.TA = User.objects.create(email = "ta@email.com", password = 'ta', is_staff = False)
        self.TA.save()
        self.Admin = User.objects.create(email = "admin@email.com", password = 'admin', is_superuser = True)
        self.Admin.save()
        self.Notification = Notification.objects.create(notification = "test", UserAllowed = self.Admin)
        self.Notification.save()

    def test_getInstructors(self):
        test = Notifications.getInstructors(self)
        self.assertEqual(list(User.objects.filter(is_superuser=False, is_staff=True)), test, msg = 'Not Equal Instructor List')

    def test_getTA(self):
        test = Notifications.getTeacherAssistants(self)
        self.assertEqual(list(User.objects.filter(is_superuser=False, is_staff=False)), test, msg = 'Not Equal TA List')

    def test_Notification(self):
        test = Notifications.getNotifications(self, self.Admin)
        self.assertEqual(list(Notification.objects.filter(UserAllowed = self.Admin)), test, msg = "Not equal notifications")