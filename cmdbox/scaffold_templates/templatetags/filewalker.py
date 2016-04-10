from __future__ import unicode_literals

from django import template
from django.utils.html import escape, mark_safe

from cmdbox.scaffold_templates.models import ScaffoldTemplate, File

register = template.Library()


@register.simple_tag
def walk(files, padding=8):
    html_buffer = ''
    for _file in files:
        is_folder = _file.file_type == File.FOLDER
        data = {
            'toggle_icon': '<span class="glyphicon glyphicon-triangle-right text-muted"></span>' if is_folder else '',
            'file_icon': 'folder-close' if is_folder else 'file',
            'file_name': _file.name,
            'padding': padding,
            'parent': _file.folder.pk if _file.folder else '',
            'id': _file.pk
        }
        html_buffer += '''<tr data-id="{id}" data-parent="{parent}">
          <td style="padding-left: {padding}px">
            <span class="toggle-folder">{toggle_icon}</span>
            <a href="">
              <span class="glyphicon glyphicon-{file_icon}"></span>
              {file_name}
            </a>
          </td>
          <td></td>
          <td></td>
          <td></td>
        </tr>'''.format(**data)
        if _file.files.exists():
            html_buffer += walk(_file.files.all(), padding + 24)
    return mark_safe(html_buffer)
