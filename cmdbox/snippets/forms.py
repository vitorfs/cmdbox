from django import forms

from cmdbox.snippets.models import Snippet
from cmdbox.snippets.validators import validate_forbidden_slug
from django.utils.translation import ugettext_lazy as _


class CreateSnippetForm(forms.ModelForm):
    slug = forms.CharField(label=_('Name'), max_length=255, required=True, help_text=_('Required slug field.'))
    description = forms.CharField(
        label=_('Description'),
        max_length=100,
        help_text=_('Give a brief description of what this snippet is about. Not required.'),
        required=False
    )

    class Meta:
        model = Snippet
        fields = ['slug', 'description', 'visibility']

    def __init__(self, user, *args, **kwargs):
        super(CreateSnippetForm, self).__init__(*args, **kwargs)
        self.instance.user = user
        self.fields['slug'].validators.append(validate_forbidden_slug)

    def clean(self):
        cleaned_data = super(CreateSnippetForm, self).clean()
        slug = cleaned_data.get('slug')
        user = self.instance.user

        if user.snippets.filter(slug=slug).exists():
            self.add_error('slug', _('A snippet with this name already exists.'))


class EditSnippetForm(forms.ModelForm):

    class Meta:
        model = Snippet
        fields = ['content', ]
