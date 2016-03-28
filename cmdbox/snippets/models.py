from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Snippet(models.Model):
    user = models.ForeignKey(User)
    slug = models.SlugField(_('slug'), max_length=255)
    description = models.TextField(_('description'), max_length=1000)
    content = models.TextField(_('content'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = 'snippet'
        verbose_name_plural = 'snippets'
        unique_together = (('user', 'slug'),)

    def __unicode__(self):
        return self.slug


class Review(models.Model):
    snippet = models.ForeignKey(Snippet, related_name='reviews')
    slug = models.SlugField(_('slug'), max_length=255)
    content = models.TextField(_('content'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    revision = models.PositiveIntegerField(_('revision'), default=1)

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ('-revision', )

    def __unicode__(self):
        return '{0} ({1})'.format(self.snippet.slug, self.revision)
