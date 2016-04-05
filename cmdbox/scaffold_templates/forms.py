from django import forms

from cmdbox.scaffold_templates.models import ScaffoldTemplate


class CreateScaffoldTemplate(forms.ModelForm):
    class Meta:
        model = ScaffoldTemplate
        fields = ['slug', 'description', 'visibility']


class EditScaffoldTemplate(forms.ModelForm):
    class Meta:
        model = ScaffoldTemplate
        fields = '__all__'
