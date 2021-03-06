import json

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.template import Context
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.utils.html import escape, mark_safe

from cmdbox.scaffold_templates.models import ScaffoldTemplate, File
from cmdbox.scaffold_templates.forms import CreateScaffoldTemplate, EditScaffoldTemplate, FileForm, EditFileContentForm
from cmdbox.scaffold_templates.templatetags.filewalker import walk


def index(request):
    return render(request, 'scaffold_templates/index.html')


@login_required
def add(request):
    if request.method == 'POST':
        form = CreateScaffoldTemplate(request.user, request.POST)
        if form.is_valid():
            scaffold_template = form.save()
            return redirect('scaffold_templates:details', scaffold_template.user.username, scaffold_template.slug)
    else:
        form = CreateScaffoldTemplate(request.user)
    return render(request, 'scaffold_templates/add.html', {'form': form})


def scaffold_templates(request, username):
    user = get_object_or_404(User, username__iexact=username)
    return render(request, 'scaffold_templates/list.html', {'page_user': user})


@ensure_csrf_cookie
def details(request, username, slug):
    try:
        scaffold_template = ScaffoldTemplate \
            .objects.select_related('user') \
            .get(user__username=username, slug=slug)
    except ScaffoldTemplate.DoesNotExist:
        raise Http404
    return render(request, 'scaffold_templates/details.html', {'scaffold_template': scaffold_template})


def _add_file(request, file_instance):
    depth = request.GET.get('depth', 0)
    json_context = dict()
    if request.method == 'POST':
        form = FileForm(request.POST, instance=file_instance)
        is_valid = json_context['is_valid'] = form.is_valid()
        if is_valid:
            _file = form.save()
            files = _file.template.files.all()
            json_context['file'] = _file.pk
            json_context['html'] = walk(files)
            json_context['itemsCount'] = files.count()
        else:
            json_context['error'] = form['name'].errors
    else:
        initial_name = _('untitled {0}').format(file_instance.get_file_type_display())
        base_name = initial_name
        i = 1
        while True:
            if File.objects \
                    .filter(name=initial_name, template=file_instance.template, folder=file_instance.folder) \
                    .exists():
                i += 1
                initial_name = '{0} {1}'.format(base_name, i)
            else:
                break
        form = FileForm(instance=file_instance, initial={'name': initial_name})
    reverse_url = request.path
    context = Context({'form': form, 'reverse_url': reverse_url, 'depth': depth})
    json_context['form'] = render_to_string('scaffold_templates/partial_file_form.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')


@login_required
def add_file(request, username, slug):
    try:
        scaffold_template = ScaffoldTemplate.objects.get(user__username=username, slug=slug)
        file_instance = File(template=scaffold_template, file_type=File.FILE)
        return _add_file(request, file_instance)
    except ScaffoldTemplate.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
def add_children_file(request, username, slug, file_id):
    try:
        scaffold_template = ScaffoldTemplate.objects.get(user__username=username, slug=slug)
        parent_folder = File.objects.get(pk=file_id, template=scaffold_template)
        file_instance = File(template=scaffold_template, file_type=File.FILE, folder=parent_folder)
        return _add_file(request, file_instance)
    except (ScaffoldTemplate.DoesNotExist, File.DoesNotExist):
        return HttpResponseBadRequest()


@login_required
def add_folder(request, username, slug):
    try:
        scaffold_template = ScaffoldTemplate.objects.get(user__username=username, slug=slug)
        folder_instance = File(template=scaffold_template, file_type=File.FOLDER)
        return _add_file(request, folder_instance)
    except ScaffoldTemplate.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
def add_children_folder(request, username, slug, file_id):
    try:
        scaffold_template = ScaffoldTemplate.objects.get(user__username=username, slug=slug)
        parent_folder = File.objects.get(pk=file_id, template=scaffold_template)
        folder_instance = File(template=scaffold_template, file_type=File.FOLDER, folder=parent_folder)
        return _add_file(request, folder_instance)
    except (ScaffoldTemplate.DoesNotExist, File.DoesNotExist):
        return HttpResponseBadRequest()


@login_required
def rename_file(request, username, slug, file_id):
    _file = get_object_or_404(File, pk=file_id, template__user__username=username, template__slug=slug)
    depth = request.GET.get('depth', 0)

    json_context = dict()

    if request.method == 'POST':
        form = FileForm(request.POST, instance=_file)
        is_valid = json_context['is_valid'] = form.is_valid()
        if is_valid:
            _file = form.save()
            json_context['file'] = _file.pk
            json_context['html'] = walk(_file.template.files.all())
        else:
            json_context['error'] = form['name'].errors
    else:
        form = FileForm(instance=_file)
        template = _file.template
        reverse_url = reverse('scaffold_templates:rename_file', args=(template.user.username, template.slug, _file.pk))
        context = Context({'form': form, 'reverse_url': reverse_url, 'depth': depth})
        json_context['form'] = render_to_string('scaffold_templates/partial_file_form.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')


@login_required
def duplicate_file(request, username, slug, file_id):
    try:
        scaffold_template = ScaffoldTemplate.objects.get(user__username=username, slug=slug)
        _file = File.objects.get(pk=file_id, template=scaffold_template)

        duplicated_file = _file.duplicate()
        files = scaffold_template.files.all()

        json_context = dict()
        json_context['file'] = duplicated_file.pk
        json_context['html'] = walk(files)
        json_context['itemsCount'] = files.count()
        return HttpResponse(json.dumps(json_context), content_type='application/json')
    except File.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
def delete_file(request, username, slug, file_id):
    try:
        _file = File.objects.get(pk=file_id, template__user__username=username, template__slug=slug)
        json_context = dict()
        if request.method == 'POST':
            _file.delete()
            files = _file.template.files.all()
            json_context['file'] = file_id
            json_context['itemsCount'] = files.count()
        else:
            context = Context({'file': _file})
            json_context['html'] = render_to_string('scaffold_templates/partial_delete_file.html', context)
        return HttpResponse(json.dumps(json_context), content_type='application/json')
    except File.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
def edit(request, username, slug):
    scaffold_template = get_object_or_404(ScaffoldTemplate, user__username=username, slug=slug)
    if request.method == 'POST':
        form = EditScaffoldTemplate(request.POST, instance=scaffold_template)
        if form.is_valid():
            scaffold_template = form.save()
            return redirect('scaffold_templates:details', scaffold_template.user.username, scaffold_template.slug)
    else:
        form = EditScaffoldTemplate(instance=scaffold_template)
    files_display_option = request.COOKIES.get('files-display-options', 'grid')
    return render(request, 'scaffold_templates/edit.html', {
        'scaffold_template': scaffold_template,
        'form': form,
        'files_display_option': files_display_option
    })


@login_required
def edit_file(request, username, slug, file_id):
    scaffold_template = get_object_or_404(ScaffoldTemplate, user__username=username, slug=slug)
    _file = get_object_or_404(File, pk=file_id, template=scaffold_template)
    if request.method == 'POST':
        form = EditFileContentForm(request.POST, instance=_file)
        if form.is_valid():
            form.save()
            message = mark_safe(
                _('The file <strong>{0}</strong> was successfully updated!').format(escape(_file.name))
            )
            messages.success(request, message)
            return redirect('scaffold_templates:edit', scaffold_template.user.username, scaffold_template.slug)
    else:
        form = EditFileContentForm(instance=_file)
    return render(request, 'scaffold_templates/edit_file.html', {'scaffold_template': scaffold_template, 'form': form})


@login_required
@require_POST
def delete(request, username, slug):
    scaffold_template = get_object_or_404(ScaffoldTemplate, user__username=username, slug=slug)
    scaffold_template.delete()
    return redirect('profile', request.user.username)
