from django import forms

from cmdbox.snippets.models import Snippet
from cmdbox.snippets.validators import validate_forbidden_slug


class CreateSnippetForm(forms.ModelForm):

    class Meta:
        model = Snippet
        fields = ['slug', 'description', 'visibility', 'content']

    def __init__(self, *args, **kwargs):
        super(CreateSnippetForm, self).__init__(*args, **kwargs)
        self.fields['slug'].validators.append(validate_forbidden_slug)

    def clean(self):
        cleaned_data = super(CreateSnippetForm, self).clean()
        slug = cleaned_data.get('slug')
        user = self.instance.user

        if user.snippets.filter(slug=slug).exists():
            self.add_error('slug', 'A snippet with this name already exists.')
