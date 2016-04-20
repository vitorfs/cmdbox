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


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('name', )

    def clean(self):
        cleaned_data = super(FileForm, self).clean()
        template = self.instance.template
        folder = self.instance.folder
        name = cleaned_data.get('name')
        files = File.objects.filter(template=template, folder=folder, name=name)
        if self.instance.pk:
            files = files.exclude(pk=self.instance.pk)
        if files.exists():
            self.add_error(
                'name',
                _('The name <strong>"{0}"</strong> is already taken. Please choose a different name.').format(name)
            )


class EditFileContentForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('content', )
