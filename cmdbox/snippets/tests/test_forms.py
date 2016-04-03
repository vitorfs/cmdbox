from model_mommy import mommy

from django.test import TestCase

from cmdbox.snippets.forms import CreateSnippetForm
from cmdbox.snippets.validators import validate_forbidden_slug


class CreateSnippetFormTests(TestCase):

    def setUp(self):
        self.user = mommy.make('auth.User', username='john')
        self.form = CreateSnippetForm(self.user)

    def test_form_has_fields(self):
        expected = ['slug', 'description', 'visibility']
        self.assertSequenceEqual(expected, list(self.form.fields))

    def test_form_has_custom_validators(self):
        self.assertTrue(validate_forbidden_slug in self.form.fields['slug'].validators)


class CreateSnippetFormIsValidTests(TestCase):

    def setUp(self):
        self.user = mommy.make('auth.User', username='john')
        form_data = {'slug': 'test2', 'description': '', 'visibility': 1}
        self.form = CreateSnippetForm(self.user, data=form_data)

    def test_form_is_valid(self):
        self.assertTrue(self.form.is_valid())


class CreateSnippetFormIsNotValid(TestCase):

    def setUp(self):
        self.user = mommy.make('auth.User', username='john')
        mommy.make('snippets.Snippet', user=self.user, slug='test')

    def test_form_is_not_valid_duplicate_key(self):
        form = CreateSnippetForm(self.user, data={'slug': 'test', 'description': '', 'visibility': 1})
        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_no_data(self):
        form = CreateSnippetForm(self.user, data=dict())
        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_forbidden_slug(self):
        form = CreateSnippetForm(self.user, data={'slug': 'templates', 'description': '', 'visibility': 1})
        self.assertFalse(form.is_valid())
