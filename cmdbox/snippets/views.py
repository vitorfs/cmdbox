from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from cmdbox.snippets.models import Snippet
from cmdbox.snippets.forms import CreateSnippetForm, EditSnippetForm


@login_required
def add(request):
    if request.method == 'POST':
        form = CreateSnippetForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', args=(request.user.username,)))
    else:
        form = CreateSnippetForm(request.user)
    return render(request, 'snippets/add.html', {'form': form})


def snippet(request, username, slug):
    _snippet = get_object_or_404(Snippet, user__username=username, slug=slug)
    return render(request, 'snippets/snippet.html', {'snippet': _snippet})


@login_required
def edit(request, username, slug):
    _snippet = get_object_or_404(Snippet, user__username=username, slug=slug)
    if request.method == 'POST':
        form = EditSnippetForm(request.POST, instance=_snippet)
        if form.is_valid():
            _snippet = form.save()
            return redirect(reverse('snippets:snippet', args=(_snippet.user.username, _snippet.slug)))
    else:
        form = EditSnippetForm(instance=_snippet)
    return render(request, 'snippets/edit.html', {'form': form})


@login_required
@require_POST
def delete(request, username, slug):
    _snippet = get_object_or_404(Snippet, user__username=username, slug=slug)
    _snippet.delete()
    return redirect(reverse('profile', args=(request.user.username, )))
