from __future__ import unicode_literals
from string import Formatter
import pyparsing

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from cmdbox.core.models import AbstractService


class Snippet(AbstractService):
    content = models.TextField(_('content'))

    class Meta:
        verbose_name = 'snippet'
        verbose_name_plural = 'snippets'
        unique_together = (('user', 'slug'), )
        ordering = ('-updated_at', )

    def __unicode__(self):
        return self.slug

    def get_cleaned_content(self):
        comment = pyparsing.nestedExpr("/*", "*/").suppress()
        cleaned_content = comment.transformString(self.content)
        return cleaned_content

    def get_params(self):
        formatter = Formatter()
        format_iterator = formatter.parse(self.get_cleaned_content())
        params = {
            'args': list(),
            'kwargs': set()
        }
        for _tuple in format_iterator:
            field_name = _tuple[1]
            if field_name is not None:
                if field_name == '':
                    params['args'].append(field_name)
                elif field_name.isdigit():
                    if field_name not in params['args']:
                        params['args'].append(field_name)
                else:
                    params['kwargs'].add(field_name)
        return params

    def use(self, args, kwargs):
        output = ''
        try:
            output = self.get_cleaned_content().format(*args, **kwargs)
            self.used += 1
            self.last_used = timezone.now()
            self.save()
        except ValueError:
            raise ValueError(_('[S02] Cannot switch from manual field specification to automatic field numbering.'))
        except IndexError:
            raise IndexError(_('[S03]'))
        except KeyError:
            raise KeyError(_('[S04]'))
        return output


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
