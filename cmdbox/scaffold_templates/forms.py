from django import forms
from django.utils.translation import ugettext_lazy as _

from cmdbox.scaffold_templates.models import ScaffoldTemplate, File
from cmdbox.core.forms import AbstractServiceCreateForm


class CreateScaffoldTemplate(AbstractServiceCreateForm):
    description = forms.CharField(
        label=_('Description'),
        max_length=100,
        help_text=_('Give a brief description of what this scaffold template is about. Not required.'),
        required=False
    )

    class Meta(AbstractServiceCreateForm.Meta):
        model = ScaffoldTemplate


class EditScaffoldTemplate(forms.ModelForm):
    class Meta:
        model = ScaffoldTemplate
        fields = '__all__'


class CreateFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('name', )

    def clean(self):
        cleaned_data = super(CreateFileForm, self).clean()
        template = self.instance.template
        folder = self.instance.folder
        name = cleaned_data.get('name')
        if File.objects.filter(template=template, folder=folder, name=name).exists():
            self.add_error(
                'name',
                _('The name "{0}" is already taken. Please choose a different name.').format(name)
            )


class RenameFileForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = File
        fields = ('id', 'name')
