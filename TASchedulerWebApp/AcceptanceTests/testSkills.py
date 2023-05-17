from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from TASchedulerWebApp.models import Skill  

class AddSkillTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_skill_url = reverse('add_skill') 
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            password='testpass123',
        )
        self.user.is_active = False
        self.user.is_staff = False
        self.user.save()

    def test_add_skill(self):
        self.client.login(email='testuser@test.com', password='testpass123')
        self.assertTrue(login)
        response = self.client.post(self.add_skill_url, {
            'skill_name': 'test skill',
        })

        self.assertEqual(response.status_code, 200)  
        self.assertTrue(Skill.objects.filter(name='test skill', TeacherAssistant=self.user).exists())
