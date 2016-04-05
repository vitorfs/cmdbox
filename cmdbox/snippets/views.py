from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from cmdbox.snippets.models import Snippet
from cmdbox.snippets.forms import CreateSnippetForm, EditSnippetForm


def index(request):
    return render(request, 'snippets/index.html')


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


def snippets(request, username):
    user = get_object_or_404(User, username__iexact=username)
    return render(request, 'snippets/list.html', {'page_user': user})


def details(request, username, slug):
    snippet = get_object_or_404(Snippet, user__username=username, slug=slug)
    return render(request, 'snippets/details.html', {'snippet': snippet})


@login_required
def edit(request, username, slug):
    snippet = get_object_or_404(Snippet, user__username=username, slug=slug)
    if request.method == 'POST':
        form = EditSnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            snippet = form.save()
            return redirect(reverse('snippets:details', args=(snippet.user.username, snippet.slug)))
    else:
        form = EditSnippetForm(instance=snippet)
    return render(request, 'snippets/edit.html', {'form': form})


@login_required
@require_POST
def delete(request, username, slug):
    snippet = get_object_or_404(Snippet, user__username=username, slug=slug)
    snippet.delete()
    return redirect(reverse('profile', args=(request.user.username, )))
