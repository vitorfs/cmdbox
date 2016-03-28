from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User)
    url = models.URLField(_('url'), null=True, blank=True)
    location = models.CharField(_('location'), max_length=255, null=True, blank=True)
    company = models.CharField(_('company'), max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'profiles'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


class SSHKey(models.Model):
    user = models.ForeignKey(User, related_name='ssh_keys')
    label = models.CharField(_('label'), max_length=255)
    fingerprint = models.CharField(_('fingerprint'), max_length=255)
    key = models.TextField(_('key'), max_length=1000)
    added_on = models.DateTimeField(_('added on'), auto_now_add=True)
    last_used = models.DateTimeField(_('last used'), null=True, blank=True)

    class Meta:
        db_table = 'ssh_keys'
        ordering = ('label', )
        verbose_name = _('ssh key')
        verbose_name_plural = _('ssh keys')
