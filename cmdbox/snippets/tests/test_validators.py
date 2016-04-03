from django.test import TestCase
from django.core.exceptions import ValidationError

from cmdbox.snippets.validators import validate_forbidden_slug


class SnippetsValidatorsTests(TestCase):

    def test_forbidden_slug_lowercase(self):
        with self.assertRaises(ValidationError):
            validate_forbidden_slug('snippets')

    def test_forbidden_slug_uppercase(self):
        with self.assertRaises(ValidationError):
            validate_forbidden_slug('SNIPPETS')
