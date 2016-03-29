from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404


def snippets(request, username):
    user = get_object_or_404(User, username__iexact=username)
    return render(request, 'snippets/snippets.html', {'page_user': user})
