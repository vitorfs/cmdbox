import json

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from cmdbox.scaffold_templates.models import ScaffoldTemplate, File
from cmdbox.scaffold_templates.forms import CreateScaffoldTemplate, EditScaffoldTemplate, CreateFileForm
from cmdbox.scaffold_templates.templatetags.filewalker import walk


def index(request):
    return render(request, 'scaffold_templates/index.html')


@login_required
def add(request):
    if request.method == 'POST':
        form = CreateScaffoldTemplate(request.user, request.POST)
        if form.is_valid():
            scaffold_template = form.save()
            return redirect(
                reverse('scaffold_templates:details', args=(scaffold_template.user.username, scaffold_template.slug))
            )
    else:
        form = CreateScaffoldTemplate(request.user)
    return render(request, 'scaffold_templates/add.html', {'form': form})


def scaffold_templates(request, username):
    user = get_object_or_404(User, username__iexact=username)
    return render(request, 'scaffold_templates/list.html', {'page_user': user})


def details(request, username, slug):
    try:
        scaffold_template = ScaffoldTemplate \
            .objects.select_related('user') \
            .get(user__username=username, slug=slug)
    except ScaffoldTemplate.DoesNotExist:
        raise Http404
    return render(request, 'scaffold_templates/details.html', {'scaffold_template': scaffold_template})


def _add_file(request, file_instance):
    json_context = dict()
    if request.method == 'POST':
        form = CreateFileForm(request.POST, prefix='add_file', instance=file_instance)
        is_valid = json_context['is_valid'] = form.is_valid()
        if is_valid:
            _file = form.save()
            json_context['file'] = _file.pk
            json_context['html'] = walk(_file.template.files.all())
            return HttpResponse(json.dumps(json_context), content_type='application/json')
    else:
        form = CreateFileForm(prefix='add_file', instance=file_instance, initial={'name': _('untitled file')})
    context = RequestContext(request, {'form': form})
    json_context['form'] = render_to_string('scaffold_templates/partial_file_form.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')


@login_required
def add_file(request, username, slug):
    try:
        scaffold_template = ScaffoldTemplate.objects.get(user__username=username, slug=slug)
        file_instance = File(template=scaffold_template)
        return _add_file(request, file_instance)
    except ScaffoldTemplate.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
def add_children_file(request, username, slug, folder_id):
    try:
        scaffold_template = ScaffoldTemplate.objects.get(user__username=username, slug=slug)
        folder = File.objects.get(pk=folder_id, template=scaffold_template)
        file_instance = File(template=scaffold_template, folder=folder)
        return _add_file(request, file_instance)
    except (ScaffoldTemplate.DoesNotExist, File.DoesNotExist):
        return HttpResponseBadRequest()


@login_required
@require_POST
def delete_file(request, username, slug, file_id):
    try:
        _file = File.objects.get(pk=file_id, template__user__username=username, template__slug=slug)
        _file.delete()
        json_context = dict()
        files = _file.template.files.all()
        json_context['html'] = walk(files)
        json_context['itemsCount'] = files.count()
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
            return redirect(
                reverse('scaffold_templates:details', args=(scaffold_template.user.username, scaffold_template.slug))
            )
    else:
        form = EditScaffoldTemplate(instance=scaffold_template)
    return render(request, 'scaffold_templates/edit.html', {'form': form})


@login_required
@require_POST
def delete(request, username, slug):
    scaffold_template = get_object_or_404(ScaffoldTemplate, user__username=username, slug=slug)
    scaffold_template.delete()
    return redirect(reverse('profile', args=(request.user.username, )))
