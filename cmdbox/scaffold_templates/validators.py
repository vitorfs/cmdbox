from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.apps import apps


def validate_folder(value):
    File = apps.get_model(app_label='scaffold_templates', model_name='File')
    _file = File.objects.get(pk=value)
    if _file.file_type != File.FOLDER:
        raise ValidationError(
            _('%(value)s is not a folder'),
            params={'value': _file.name},
        )
