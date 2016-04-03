from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from cmdbox.snippets.models import Snippet
from cmdbox.snippets.forms import CreateSnippetForm


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


@login_required
def snippet(request, username, slug):
    _snippet = get_object_or_404(Snippet, user__username=username, slug=slug)
    return render(request, 'snippets/snippet.html', {'snippet': _snippet})


@login_required
def edit(request, username, slug):
    _snippet = get_object_or_404(Snippet, user__username=username, slug=slug)
    return render(request, 'snippets/edit.html', {'snippet': _snippet})


@login_required
def delete(request, username, slug):
    pass
