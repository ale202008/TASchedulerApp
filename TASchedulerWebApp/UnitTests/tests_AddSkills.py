from django.test import TestCase, Client
from django.contrib.auth.models import User
from TASchedulerWebApp.models import Skill
from django.urls import reverse

class AddSkillTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('username', 'email@test.com', 'password')
        self.skill_name = 'skill1'
        self.add_skill_url = reverse('add_skill') # the name you've given to the add_skill path in your urls

    def test_add_skill(self):
        self.client.login(username='username', password='password')

        response = self.client.post(self.add_skill_url, {'skill_name': self.skill_name})
        self.assertEqual(response.status_code, 302)  # assuming it should redirect, hence 302

        skills = Skill.objects.filter(name=self.skill_name)
        self.assertEqual(skills.count(), 1)  # checks that the skill was created

        # ensure that the user is now associated with the created skill
        self.assertTrue(skills.first().TeacherAssistant.filter(id=self.user.id).exists())
