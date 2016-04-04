# coding: utf-8

from __future__ import unicode_literals
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

    def test_get_cleaned_content_3(self):
        self.snippet.content = 'éçñø§^à'
        expected = 'éçñø§^à'
        actual = self.snippet.get_cleaned_content()
        self.assertEqual(expected, actual)

    def test_get_params_with_kwargs(self):
        self.snippet.content = 'This is a {test} {formating} with kwargs'
        expected = {'args': list(), 'kwargs': set(['test', 'formating'])}
        actual = self.snippet.get_params()
        self.assertEqual(expected, actual)

    def test_get_params_with_args(self):
        self.snippet.content = 'This is a {0} {1} with args'
        expected = {'args': ['0', '1'], 'kwargs': set()}
        actual = self.snippet.get_params()
        self.assertEqual(expected, actual)

    def test_get_params_with_args_duplicate_key(self):
        self.snippet.content = '{0}{1}{0}'
        expected = {'args': ['0', '1'], 'kwargs': set()}
        actual = self.snippet.get_params()
        self.assertEqual(expected, actual)

    def test_get_params_with_positional_args(self):
        self.snippet.content = 'This is a {} {} with args'
        expected = {'args': ['', ''], 'kwargs': set()}
        actual = self.snippet.get_params()
        self.assertEqual(expected, actual)

    def test_get_params_with_args_and_kwargs(self):
        self.snippet.content = 'This is a {test} {format} {0} {1} with args and kwargs'
        expected = {'args': ['0', '1'], 'kwargs': set(['test', 'format'])}
        actual = self.snippet.get_params()
        self.assertEqual(expected, actual)

    def test_use(self):
        self.snippet.content = 'This is a usage {test} with {format}'
        expected = 'This is a usage lorem with ipsum'
        actual = self.snippet.use(list(), {'test': 'lorem', 'format': 'ipsum'})
        self.assertEqual(expected, actual)
        self.assertEqual(1, self.snippet.used)

    def test_use_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.snippet.content = '{0}{}'
            self.snippet.use(['a', 'b'], dict())

    def test_use_raises_index_error(self):
        with self.assertRaises(IndexError):
            self.snippet.content = '{0}'
            self.snippet.use(list(), dict())

    def test_use_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.snippet.content = '{kwarg}'
            self.snippet.use(list(), dict())
