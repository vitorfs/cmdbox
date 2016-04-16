from __future__ import unicode_literals
import os.path

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cmdbox.core.models import AbstractService
from cmdbox.scaffold_templates.validators import validate_folder


class ScaffoldTemplate(AbstractService):

    class Meta:
        verbose_name = _('scaffold template')
        verbose_name_plural = _('scaffold template')
        unique_together = (('user', 'slug'), )
        ordering = ('-updated_at', )


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
    folder = models.ForeignKey('File', null=True, blank=True, related_name='files', validators=[validate_folder, ])
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

    def save(self, *args, **kwargs):
        self.extension = os.path.splitext(self.name)[1][1:].strip()[:10]
        return super(File, self).save(args, kwargs)

    def is_folder(self):
        return self.file_type == File.FOLDER

    def duplicate(self):
        copy = self
        copy.pk = None
        base_name, extension = os.path.splitext(self.name)
        base_copy_text = _('copy')

        copy_text = ' {0}'.format(base_copy_text)
        name = ''
        copy_number = 1
        while True:
            if len(extension) > 11:
                max_length = 255 - len(copy_text)
                name = '{0}{1}'.format(self.name[:max_length], extension)
            else:
                max_length = 255 - len(extension) - len(copy_text)
                name = '{0}{1}{2}'.format(base_name[:max_length], copy_text, extension)

            if not File.objects.filter(name=name, template=self.template, folder=self.folder).exists():
                break
            else:
                copy_number += 1
                copy_text = ' {0} {1}'.format(base_copy_text, copy_number)

        copy.name = name
        copy.save()
        return copy

