from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from cmdbox.scaffold_templates.models import ScaffoldTemplate
from cmdbox.scaffold_templates.forms import CreateScaffoldTemplate, EditScaffoldTemplate


def index(request):
    return render(request, 'scaffold_templates/index.html')


@login_required
def add(request):
    if request.method == 'POST':
        form = CreateScaffoldTemplate(request.POST)
        if form.is_valid():
            scaffold_template = form.save()
            return redirect(
                reverse('scaffold_templates:details', args=(scaffold_template.user.username, scaffold_template.slug))
            )
    else:
        form = CreateScaffoldTemplate()
    return render(request, 'scaffold_templates/add.html', {'form': form})


def scaffold_templates(request, username):
    user = get_object_or_404(User, username__iexact=username)
    return render(request, 'scaffold_templates/list.html', {'page_user': user})


@login_required
def details(request, username, slug):
    scaffold_template = get_object_or_404(ScaffoldTemplate, user__username=username, slug=slug)
    return render(request, 'scaffold_templates/details.html', {'scaffold_template': scaffold_template})


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
