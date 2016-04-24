from social.apps.django_app.default.models import UserSocialAuth

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from cmdbox.profiles.forms import UserForm, ProfileForm, ChangeUsernameForm


@login_required
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def account(request):
    # Create a new instance of user to avoid changing the request.user instance
    # before actually persisting the changes.
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your username was successfully updated!'))
            return redirect('settings:account')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = ChangeUsernameForm(instance=user)
    return render(request, 'profiles/account.html', {'form': form})


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('settings:password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordForm(request.user)
    return render(request, 'profiles/change_password.html', {'form': form})


@login_required
def logins(request):
    try:
        github_login = request.user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        twitter_login = request.user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    can_disconnect = (request.user.social_auth.count() > 1 or request.user.has_usable_password())
    return render(request, 'profiles/logins.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'can_disconnect': can_disconnect
    })
