from django.test import TestCase
import collab.tc_library as tc_lib
from django.contrib import auth
from collab.models import Project
from django.contrib.auth.models import User
from accounts.models import UserProfile, Request
from django.urls import reverse

TEST_PROJECTS = [
    {'title': 'Test Project', 'city': 'Las Vegas', 'description': 'A big time test project with lots of momentum and people wanting to help.',
     'skills_needed': 'Java, Python, HTML'}
]
TEST_USERS = [
    {'username': 'testuser_emptyprofile', 'email': 'test.a@gmail.com', 'password': '1234pass'},
    {'username': 'testuser_a', 'email': 'test.b@gmail.com', 'password': '1234pass'},
    {'username': 'testuser_b', 'email': 'test.c@gmail.com', 'password': '1234pass'}
]
TEST_PROFILES = [
    {'name': 'Test Profile A', 'pronouns': 'he/him', 'city': 'Las Vegas', 'skills': 'Java, Python',
     'email': 'contact.email.a@gmail.com', 'phone': '7022345678', 'picture': '',
     'bio': 'In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available.'},

    {'name': 'Test Profile B', 'pronouns': 'they/them', 'city': 'New York City', 'skills': 'JavaScript, Java, Python, HTML, Ruby',
     'email': 'contact.email.b@gmail.com', 'phone': '7572345678', 'picture': '',
     'bio': 'In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available.'}
]


class LogicTests(TestCase):

    def setUp(self):  # Python's builtin unittest for db entries

        # create users
        for u in TEST_USERS:
            user = User.objects.create_user(username=u['username'], email=u['email'], password=u['password'])
            user.save()

        # login user
        self.client.login(username=TEST_USERS[0]['username'], password=TEST_USERS[0]['password'])
        user_id = auth.get_user(self.client).id

        # populate user profile
        response = self.client.post(reverse('accounts:profile-update', args=[str(user_id)]), {**TEST_PROFILES[0]}, follow=True)
        city = UserProfile.objects.get(user=user_id).city

        '''
        user = User.objects.get(username=TEST_USERS[1]['username'])
        user.userprofile.name = TEST_PROFILES[0]['name']
        user.userprofile.pronouns = TEST_PROFILES[0]['pronouns']
        user.userprofile.city = TEST_PROFILES[0]['city']
        user.userprofile.email = TEST_PROFILES[0]['email']
        user.userprofile.phone = TEST_PROFILES[0]['phone']
        user.userprofile.picture = TEST_PROFILES[0]['picture']
        user.userprofile.bio = TEST_PROFILES[0]['bio']
        user.save()
        '''

    def test_profile_populated(self):
        user = User.objects.get(username=TEST_USERS[0]['username'])
        city = UserProfile.objects.get(user=user.id).city
        self.assertEqual(city, TEST_PROFILES[0]['city'])

    def test_view_project(self):
        response = self.client.get(reverse('project'), {'id': user})
        self.assertEqual(response.status_code, 200)

    def test_generate_user_matches(self):
        pass

