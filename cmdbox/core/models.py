from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractService(models.Model):
    PUBLIC = 1
    UNLISTED = 2
    PRIVATE = 3

    VISIBILITY_CHOICES = (
        (PUBLIC, _('Public')),
        (UNLISTED, _('Unlisted')),
        (PRIVATE, _('Private')),
    )

    user = models.ForeignKey(User, related_name='%(class)ss')
    slug = models.SlugField(_('name'), max_length=255)
    description = models.CharField(_('description'), max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), null=True, blank=True)
    last_used = models.DateTimeField(_('last used'), null=True, blank=True)
    visibility = models.PositiveSmallIntegerField(_('visibility'), choices=VISIBILITY_CHOICES, default=PUBLIC)
    version = models.PositiveIntegerField(_('version'), default=1)
    stars = models.PositiveIntegerField(_('stars'), default=0)
    used = models.PositiveIntegerField(_('used'), default=0)
    language = models.CharField(_('language'), max_length=50, null=True, blank=True)

    class Meta:
        abstract = True


class FileSystemObject(models.Model):
    name = models.CharField(_('name'), max_length=255)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ('name', )

    def __unicode__(self):
        return self.name
