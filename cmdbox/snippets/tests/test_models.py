from model_mommy import mommy

from django.test import TestCase

from cmdbox.snippets.models import Snippet, Review


class SnippetsModelsTests(TestCase):
    def setUp(self):
        self.snippet = mommy.make(Snippet, slug='test-snippet')
        self.review = mommy.make(Review, snippet=self.snippet, revision=1)

    def test_snippet_unicode(self):
        self.assertTrue(isinstance(self.snippet, Snippet))
        self.assertEqual(self.snippet.__unicode__(), 'test-snippet')

    def test_review_unicode(self):
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(self.review.__unicode__(), 'test-snippet (1)')

    def test_get_cleaned_content(self):
        self.snippet.content = '/* comment */test content'
        expected = 'test content'
        actual = self.snippet.get_cleaned_content()
        self.assertEqual(expected, actual)

    def test_get_cleaned_content_2(self):
        self.snippet.content = '/* comment */test content="/*"'
        expected = 'test content="/*"'
        actual = self.snippet.get_cleaned_content()
        self.assertEqual(expected, actual)
