from __future__ import unicode_literals

from django import template
from django.utils.html import mark_safe
from django.template.loader import render_to_string

register = template.Library()


def _walk(files, parent, depth):
    html_buffer = ''
    children_files = filter(lambda f: f.folder == parent, files)
    for _file in children_files:
        html_buffer += render_to_string('scaffold_templates/partial_file.html', {'file': _file, 'depth': depth})
        html_buffer += _walk(files, _file, depth + 1)
    return html_buffer


@register.simple_tag
def walk(files):
    files = files.select_related('folder')
    html_output = _walk(files, parent=None, depth=0)
    return mark_safe(html_output)
