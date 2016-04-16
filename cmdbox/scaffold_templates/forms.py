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
    folder = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=File.objects.filter(file_type=File.FOLDER),
        required=False
    )
    template = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=ScaffoldTemplate.objects.all(),
        required=False
    )

    class Meta:
        model = File
        fields = ('name', 'folder', 'template', )


class RenameFileForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = File
        fields = ('id', 'name')
