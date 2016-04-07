from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from cmdbox.core.validators import validate_forbidden_slug


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        help_text='Not required. The email address will only be used for password reset.',
        max_length=254,
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class AbstractServiceCreateForm(forms.ModelForm):
    slug = forms.CharField(label=_('Name'), max_length=255, required=True, help_text=_('Required slug field.'))

    class Meta:
        fields = ['slug', 'description', 'visibility']

    def __init__(self, user, *args, **kwargs):
        super(AbstractServiceCreateForm, self).__init__(*args, **kwargs)
        self.instance.user = user
        self.fields['slug'].validators.append(validate_forbidden_slug)

    def clean(self):
        cleaned_data = super(AbstractServiceCreateForm, self).clean()
        user = self.instance.user
        slug = cleaned_data.get('slug')
        if user.snippets.filter(slug=slug).exists() or user.scaffoldtemplates.filter(slug=slug).exists():
            self.add_error('slug', _('A snippet or scaffold template with this name already exists.'))
