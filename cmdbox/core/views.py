from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from cmdbox.core.forms import SignupForm
from cmdbox.snippets import views as snippets_views


def home(request):
    return render(request, 'core/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})


def profile(request, username):
    return snippets_views.snippets(request, username)
