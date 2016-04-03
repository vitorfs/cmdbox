from model_mommy import mommy

from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User
from django.test import TestCase

from cmdbox.snippets.models import Snippet


class SnippetsDeleteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.snippet = mommy.make('snippets.Snippet', slug='test', user=self.user)
        self.response = self.client.post(r('snippets:delete', args=(self.user.username, self.snippet.slug)))

    def test_post(self):
        self.assertEqual(self.response.status_code, 302)

    def test_deleted_snippet(self):
        self.assertFalse(Snippet.objects.filter(user__username='john', slug='test').exists())
