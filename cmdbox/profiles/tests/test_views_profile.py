from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User
from django.test import TestCase


class ProfilesProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.response = self.client.get(r('profile', args=('john', )))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)
