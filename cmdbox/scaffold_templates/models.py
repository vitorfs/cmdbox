from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cmdbox.core.models import AbstractService, FileSystemObject


class ScaffoldTemplate(AbstractService):

    class Meta:
        verbose_name = _('scaffold template')
        verbose_name_plural = _('scaffold template')
        unique_together = (('user', 'slug'), )
        ordering = ('-updated_at', )


class Folder(FileSystemObject):
    template = models.ForeignKey(ScaffoldTemplate, related_name='folders')

    class Meta:
        verbose_name = _('folder')
        verbose_name_plural = _('folders')
        unique_together = (('template', 'name'), )


class File(FileSystemObject):
    template = models.ForeignKey(ScaffoldTemplate, related_name='files')
    folder = models.ForeignKey(Folder, null=True, blank=True, related_name='files')
    extension = models.CharField(_('extension'), max_length=10, null=True, blank=True)
    size = models.PositiveIntegerField(_('size'), default=0)

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
        unique_together = (('template', 'name'), )
