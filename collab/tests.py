from django.test import TestCase
import collab.tc_library as tc_lib


class URLTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_adminpage(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)


'''
class TCLibraryTests(TestCase):

    def test_generateusermatches(self):
        pass
'''

