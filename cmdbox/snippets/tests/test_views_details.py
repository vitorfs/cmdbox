from model_mommy import mommy

from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User
from django.test import TestCase


class SnippetsDetailsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.snippet = mommy.make('snippets.Snippet', slug='test', description='This is a test.', user=self.user)
        self.response = self.client.get(r('snippets:details', args=(self.user.username, self.snippet.slug)))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'snippets/details.html')

    def test_html(self):
        self.assertContains(self.response, 'This is a test.')
        self.assertContains(self.response, ' href="/john/snippets/test/edit/"')
        self.assertContains(self.response, ' href="/john/snippets/test/delete/"')


class SnippetsSnippetAnonymousUserTests(TestCase):
    def setUp(self):
        self.snippet = mommy.make('snippets.Snippet', slug='table', user__username='peter')
        self.response = self.client.get(r('snippets:details', args=(self.snippet.user.username, self.snippet.slug)))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'snippets/details.html')

    def test_html(self):
        self.assertContains(self.response, ' href="/peter/snippets/table/edit/"', 0)
        self.assertContains(self.response, ' href="/peter/snippets/table/delete/"', 0)


class SnippetsSnippetNotSnippetUserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.snippet = mommy.make('snippets.Snippet', slug='table', user__username='peter')
        self.response = self.client.get(r('snippets:details', args=(self.snippet.user.username, self.snippet.slug)))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'snippets/details.html')

    def test_html(self):
        self.assertContains(self.response, ' href="/peter/snippets/table/edit/"', 0)
        self.assertContains(self.response, ' href="/peter/snippets/table/delete/"', 0)


class SnippetsSnippet404Tests(TestCase):
    def setUp(self):
        self.response = self.client.get(r('snippets:details', args=('john', 'test404')))

    def test_get(self):
        self.assertEqual(self.response.status_code, 404)
