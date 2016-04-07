from django import forms
from django.utils.translation import ugettext_lazy as _

from cmdbox.snippets.models import Snippet
from cmdbox.core.forms import AbstractServiceCreateForm


class CreateSnippetForm(AbstractServiceCreateForm):
    description = forms.CharField(
        label=_('Description'),
        max_length=100,
        help_text=_('Give a brief description of what this snippet is about. Not required.'),
        required=False
    )

    class Meta(AbstractServiceCreateForm.Meta):
        model = Snippet


class EditSnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['content', ]
