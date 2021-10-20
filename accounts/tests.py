from django.test import TestCase
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import UserProfile, Request
from taggit.models import Tag
from django.urls import reverse


TEST_USERS = [
    {'username': 'testuser_emptyprofile', 'email': 'test.a@gmail.com', 'password': '1234pass'},
    {'username': 'testuser_a', 'email': 'test.b@gmail.com', 'password': '1234pass'},
    {'username': 'testuser_b', 'email': 'test.c@gmail.com', 'password': '1234pass'}
]
TEST_PROFILES = [
    {'name': 'Test Profile A', 'pronouns': 'he/him', 'city': 'Las Vegas',
     'email': 'contact_email@gmail.com', 'phone': '7022345678', 'picture': '',
     'bio': 'In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available.'}
]


class URLTests(TestCase):

    def test_register_url(self):
        response = self.client.get(reverse('accounts:register'), follow=True)  # follow redirects
        self.assertEqual(response.status_code, 200)

    def test_login_url_get(self):
        response = self.client.get(reverse('accounts:login'), follow=True)
        self.assertEqual(response.status_code, 200)


class UserTests(TestCase):

    def setUp(self):  # Python's builtin unittest for db entries

        # create users
        for u in TEST_USERS:
            user = User.objects.create_user(username=u['username'], email=u['email'], password=u['password'])
            user.save()



    def test_users_exist(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, len(TEST_USERS))

    def test_profile_populated(self):
        # profile = UserProfile.objects.get(user__username=TEST_USERS[1]['username'])
        user = User.objects.get(username=TEST_USERS[1]['username'])
        print('user id:', user.id)
        # user.userprofile = TEST_PROFILES[0]
        user.userprofile.city = 'Las Vegas'
        user.save()

        city = UserProfile.objects.get(user=user.id).city
        print('prof city:', city)
        self.assertEqual(city, TEST_PROFILES[0]['city'])

    def test_register(self):
        data = {'username': TEST_USERS[1]['username'],
                'password': TEST_USERS[1]['password'],
                'email': TEST_USERS[1]['email']}
        response = self.client.post(reverse('accounts:register'), data, follow=True)
        user = User.objects.filter(username=TEST_USERS[1]['username'])
        self.assertEqual(user[0].username, TEST_USERS[1]['username'])
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        data = {'username': TEST_USERS[0]['username'], 'password': TEST_USERS[0]['password']}
        response = self.client.post(reverse('accounts:login'), data, follow=True)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username=TEST_USERS[1]['username'], password=TEST_USERS[0]['password'])
        user_1 = auth.get_user(self.client)
        self.assertTrue(user_1.is_authenticated)
        response = self.client.get(reverse('accounts:logout'), follow=True)
        user_2 = auth.get_user(self.client)
        self.assertNotEqual(user_1, user_2)
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        response = self.client.get(reverse('accounts:dashboard'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/dashboard/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.client.login(username=TEST_USERS[1]['username'], password=TEST_USERS[0]['password'])
        user_id = auth.get_user(self.client).id
        response = self.client.get(reverse('accounts:dashboard'), {'user': user_id}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        user_empty_profile = User.objects.filter(username=TEST_USERS[0]['username'])[0]
        response = self.client.get(reverse('accounts:profile', args=[user_empty_profile]), follow=True)
        self.assertEqual(response.status_code, 200)
