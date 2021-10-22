from django.test import TestCase
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import UserProfile, Request
from taggit.models import Tag
from django.urls import reverse


TEST_USERS = [
    {'username': 'testuser_a', 'email': 'test.b@gmail.com', 'password': 'a1234pass'},
    {'username': 'testuser_b', 'email': 'test.c@gmail.com', 'password': 'b1234pass'}
]
TEST_NEW_USERS = [
    {'username': 'testuser_c', 'email': 'test.c@gmail.com', 'password': 'c1234pass'},
    {'username': 'testuser_d', 'email': 'test.d@gmail.com', 'password': 'd1234pass'}
]
TEST_PROFILES = [
    {'name': 'Test Profile A', 'pronouns': 'he/him', 'city': 'Las Vegas', 'skills': 'Java, Python',
     'email': 'contact.email.a@gmail.com', 'phone': '7022345678', 'picture': '',
     'bio': 'In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available.'},

    {'name': 'Test Profile B', 'pronouns': 'they/them', 'city': 'New York City', 'skills': 'JavaScript, Java, Python, HTML, Ruby',
     'email': 'contact.email.b@gmail.com', 'phone': '7572345678', 'picture': '',
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

    def test_users_exist(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, len(TEST_USERS))


    def test_register(self):
        data = {'username': TEST_NEW_USERS[0]['username'],
                'password': TEST_NEW_USERS[0]['password'],
                'email': TEST_NEW_USERS[0]['email']}
        response = self.client.post(reverse('accounts:register'), data, follow=True)
        user = User.objects.filter(username=TEST_NEW_USERS[0]['username'])[0]
        self.assertEqual(user.username, TEST_NEW_USERS[0]['username'])
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        data = {'username': TEST_USERS[0]['username'], 'password': TEST_USERS[0]['password']}
        response = self.client.post(reverse('accounts:login'), data, follow=True)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username=TEST_USERS[1]['username'], password=TEST_USERS[1]['password'])
        user_1 = auth.get_user(self.client)
        self.assertTrue(user_1.is_authenticated)
        response = self.client.get(reverse('accounts:logout'), follow=True)
        user_2 = auth.get_user(self.client)
        self.assertNotEqual(user_1, user_2)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_unauthenticated(self):
        response = self.client.get(reverse('accounts:dashboard'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/dashboard/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_dashboard_auth(self):
        self.client.login(username=TEST_USERS[1]['username'], password=TEST_USERS[1]['password'])
        user_id = auth.get_user(self.client).id
        response = self.client.get(reverse('accounts:dashboard'), {'user': user_id}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_empty_profile(self):
        user_empty_profile = User.objects.filter(username=TEST_USERS[0]['username'])[0]
        response = self.client.get(reverse('accounts:profile', args=[user_empty_profile]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_profile(self):
        self.client.login(username=TEST_USERS[0]['username'], password=TEST_USERS[0]['password'])
        user_id = auth.get_user(self.client).id
        response = self.client.post(reverse('accounts:profile-update', args=[str(user_id)]), {**TEST_PROFILES[0]}, follow=True)
        city = UserProfile.objects.get(user=user_id).city
        print('prof city:', city)
        self.assertEqual(city, TEST_PROFILES[0]['city'])
        self.assertEqual(response.status_code, 200)
