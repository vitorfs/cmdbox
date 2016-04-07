from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


FORBIDDEN_SLUG = ('snippets', 'templates', 'scripts', )


def validate_forbidden_slug(value):
    if value.lower() in FORBIDDEN_SLUG:
        raise ValidationError(_('This is a reserved word.'))
