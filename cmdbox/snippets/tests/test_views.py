from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User
from django.test import TestCase

from cmdbox.snippets.models import Snippet


class SnippetsAddTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.response = self.client.get(r('snippets:add'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'snippets/add.html')

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'type="hidden"', 1)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="radio"', 3)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class SnippetsAddValidPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        data = {'slug': 'test', 'description': 'Test snippet', 'visibility': 1}
        self.response = self.client.post(r('snippets:add'), data)

    def test_post(self):
        self.assertEqual(self.response.status_code, 302)

    def test_created_snippet(self):
        self.assertTrue(Snippet.objects.filter(user__username='john', slug='test').exists())
