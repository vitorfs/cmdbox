from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from cmdbox.profiles.forms import UserForm, ProfileForm


@login_required
@transaction.atomic
def account_settings(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse('account_settings'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/account_settings.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/change_password.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username__iexact=username)
    return render(request, 'profiles/profile.html', {'page_user': user})
