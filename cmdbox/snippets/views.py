from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from cmdbox.snippets.models import Snippet
from cmdbox.snippets.forms import CreateSnippetForm


def add(request):
    if request.method == 'POST':
        form = CreateSnippetForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', args=(request.user.username,)))
    else:
        form = CreateSnippetForm()
    return render(request, 'snippets/add.html', {'form': form})


def snippet(request, username, slug):
    _snippet = get_object_or_404(Snippet, user__username=username, slug=slug)
    return render(request, 'snippets/snippet.html', {'snippet': _snippet})
