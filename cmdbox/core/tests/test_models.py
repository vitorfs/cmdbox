from __future__ import unicode_literals

from django.test import TestCase

from cmdbox.core.models import FileSystemObject


class ConcreteFileSystemObject(FileSystemObject):
    pass


class SnippetsModelsTests(TestCase):
    def setUp(self):
        self.fso = ConcreteFileSystemObject(name='test')

    def test_file_system_object_unicode(self):
        self.assertTrue(isinstance(self.fso, FileSystemObject))
        self.assertEqual(self.fso.__unicode__(), 'test')
