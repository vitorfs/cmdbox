from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Snippet(models.Model):
    PUBLIC = 1
    UNLISTED = 2
    PRIVATE = 3

    VISIBILITY_CHOICES = (
        (PUBLIC, _('Public')),
        (UNLISTED, _('Unlisted')),
        (PRIVATE, _('Private')),
    )

    user = models.ForeignKey(User, related_name='snippets')
    slug = models.SlugField(
        _('name'),
        max_length=255,
        help_text='Required slug field.'
    )
    description = models.CharField(
        _('description'),
        max_length=100,
        null=True,
        blank=True,
        help_text=_('Give a brief description of what this snippet is about. Not required.')
    )
    content = models.TextField(_('content'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    visibility = models.PositiveSmallIntegerField(_('visibility'), choices=VISIBILITY_CHOICES, default=PUBLIC)
    version = models.PositiveIntegerField(_('version'), default=1)
    stars = models.PositiveIntegerField(_('stars'), default=0)
    used = models.PositiveIntegerField(_('used'), default=0)
    language = models.CharField(_('language'), max_length=50, null=True, blank=True)
    last_used = models.DateTimeField(_('last used'), null=True, blank=True)

    class Meta:
        verbose_name = 'snippet'
        verbose_name_plural = 'snippets'
        unique_together = (('user', 'slug'), )
        ordering = ('-updated_at', )

    def __unicode__(self):
        return self.slug


class Review(models.Model):
    snippet = models.ForeignKey(Snippet, related_name='reviews')
    content = models.TextField(_('content'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    revision = models.PositiveIntegerField(_('revision'), default=1)

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ('-revision', )

    def __unicode__(self):
        return '{0} ({1})'.format(self.snippet.slug, self.revision)
