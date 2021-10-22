from django.test import TestCase
import collab.tc_library as tc_lib
from django.contrib import auth
from collab.models import Project
from django.contrib.auth.models import User
from accounts.models import UserProfile, Request
from django.urls import reverse

TEST_NEW_PROJECTS = [
    {'title': 'Test New Project', 'city': 'Tampa', 'description': 'A huge project with lots of momentum and people wanting to help.',
     'skills_needed': 'JavaScript, Ruby'}
]
TEST_PROJECTS = [
    {'title': 'Test Project', 'city': 'Las Vegas', 'description': 'A big time test project with lots of momentum and people wanting to help.',
     'skills_needed': 'Java, Python, HTML'},
    {'title': 'Test Update Project', 'city': 'Reno', 'description': 'A big time test project with lots of momentum and people wanting to help.',
     'skills_needed': 'Java, Python, HTML', 'archived': 'False'}
]
TEST_USERS = [
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


class URLTests(TestCase):

    def test_home_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_admin_url(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)


class ProjectTests(TestCase):

    def setUp(self):  # Python's builtin unittest for db entries

        # create users
        for u in TEST_USERS:
            user = User.objects.create_user(username=u['username'], email=u['email'], password=u['password'])
            user.save()

        # create project
        user = User.objects.get(username=TEST_USERS[0]['username'])
        TEST_PROJECTS[0]['founder'] = user
        Project.objects.create(**TEST_PROJECTS[0])

        # login user
        self.client.login(username=TEST_USERS[0]['username'], password=TEST_USERS[0]['password'])

    def test_projects_exist(self):
        project_count = Project.objects.all().count()
        self.assertNotEqual(project_count, 0)

    def test_update_project(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        # get project 0 to update
        project = Project.objects.filter(title=TEST_PROJECTS[0]['title'])[0]
        print('update proj:', project)
        # update with different project data
        TEST_PROJECTS[1]['founder'] = user  # add founder (logged in user)
        response = self.client.post('/collab/project/update/' + str(project.id), {**TEST_PROJECTS[1]}, follow=True)
        self.assertEqual(response.status_code, 200)
        upd_proj = Project.objects.filter(title=TEST_PROJECTS[1]['title'])[0]
        print('updated project:', upd_proj)
        city = upd_proj.city
        self.assertEqual(city, TEST_PROJECTS[1]['city'])

    def test_add_project(self):
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        # test get add project form
        response = self.client.get(reverse('collab:project-add'), {'founder': user})
        self.assertEqual(response.status_code, 200)
        # test post update project
        TEST_NEW_PROJECTS[0]['founder'] = user
        response = self.client.post(reverse('collab:project-add'), {**TEST_NEW_PROJECTS[0]}, follow=True)
        self.assertEqual(response.status_code, 200)
        project = Project.objects.filter(title=TEST_NEW_PROJECTS[0]['title'])[0]
        self.assertEqual(project.city, TEST_NEW_PROJECTS[0]['city'])

    def test_view_project(self):
        project = Project.objects.all()[0]
        print('project obj:', project)
        response = self.client.get('/collab/' + str(project.id), follow=True)
        self.assertEqual(response.status_code, 200)

