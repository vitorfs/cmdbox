from model_mommy import mommy

from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User
from django.test import TestCase

from cmdbox.snippets.models import Snippet
from cmdbox.snippets.forms import EditSnippetForm


class SnippetsEditTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.snippet = mommy.make('snippets.Snippet', slug='test', user=self.user)
        self.response = self.client.get(r('snippets:edit', args=(self.user.username, self.snippet.slug)))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'snippets/edit.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, EditSnippetForm)

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<textarea name="content"', 1)
        self.assertContains(self.response, '<div id="content"', 1)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class SnippetsEditValidPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.snippet = mommy.make('snippets.Snippet', slug='test', user=self.user, content='Old content.')
        self.response = self.client.post(
            r('snippets:edit', args=(self.user.username, self.snippet.slug)),
            {'content': 'New content.'}
        )

    def test_post(self):
        self.assertEqual(self.response.status_code, 302)

    def test_updated_snippet(self):
        snippet = Snippet.objects.get(user__username='john', slug='test')
        self.assertTrue(snippet.content == 'New content.')


class SnippetsEditInvalidPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.snippet = mommy.make('snippets.Snippet', slug='test', user=self.user)
        self.response = self.client.post(
            r('snippets:edit', args=(self.user.username, self.snippet.slug)),
            dict()
        )

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'snippets/edit.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, EditSnippetForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)
