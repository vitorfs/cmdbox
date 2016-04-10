from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cmdbox.core.models import AbstractService


class ScaffoldTemplate(AbstractService):

    class Meta:
        verbose_name = _('scaffold template')
        verbose_name_plural = _('scaffold template')
        unique_together = (('user', 'slug'), )
        ordering = ('-updated_at', )

    def get_files(self, folder=None):
        return self.files.filter(folder=folder).prefetch_related('files')

    def get_files_count(self):
        return self.files.filter(file_type=File.FILE).count()


class File(models.Model):
    FILE = 1
    FOLDER = 2
    FILE_TYPES = (
        (FILE, _('File')),
        (FOLDER, _('Folder'))
    )

    name = models.CharField(_('name'), max_length=255)
    extension = models.CharField(_('extension'), max_length=10, null=True, blank=True)
    size = models.PositiveIntegerField(_('size'), default=0)
    template = models.ForeignKey(ScaffoldTemplate, related_name='files')
    folder = models.ForeignKey('File', null=True, blank=True, related_name='files')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    file_type = models.PositiveSmallIntegerField(_('file type'), choices=FILE_TYPES, default=FILE)

    class Meta:
        ordering = ('-file_type', 'name', )
        verbose_name = _('file')
        verbose_name_plural = _('files')
        unique_together = (('template', 'folder', 'name'), )

    def __unicode__(self):
        return self.name