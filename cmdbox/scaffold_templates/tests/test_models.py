# coding: utf-8

from __future__ import unicode_literals
from model_mommy import mommy

from django.test import TestCase

from cmdbox.scaffold_templates.models import File


class FileModelTests(TestCase):
    def setUp(self):
        self.file = mommy.make(File)

    def test__get_name_parts_valid_extension(self):
        self.file.name = 'test.py'
        self.assertEqual(self.file._get_name_parts(), ('test', '.py'))

    def test__get_name_parts_valid_extension_with_unicode(self):
        self.file.name = 'tést.py'
        self.assertEqual(self.file._get_name_parts(), ('tést', '.py'))

    def test__get_name_parts_valid_extension_with_space(self):
        self.file.name = 'test .py'
        self.assertEqual(self.file._get_name_parts(), ('test ', '.py'))

    def test__get_name_parts_invalid_extension_ending_with_dot(self):
            self.file.name = 'test..'
            self.assertEqual(self.file._get_name_parts(), ('test..', ''))

    def test__get_name_parts_invalid_extension_11_length(self):
            self.file.name = 'test.areallybige'
            self.assertEqual(self.file._get_name_parts(), ('test.areallybige', ''))

    def test__get_name_parts_name_starting_with_dot(self):
            self.file.name = '.env'
            self.assertEqual(self.file._get_name_parts(), ('.env', ''))

    def test__get_name_parts_name_with_space_before_extension(self):
            self.file.name = 'name.. copy 2.txt'
            self.assertEqual(self.file._get_name_parts(), ('name.. copy 2', '.txt'))
