from django.contrib.auth.models import User


def get_username(strategy, details, user=None, *args, **kwargs):
    if not user:
        username = details['username']
        i = 0
        while User.objects.filter(username__iexact=username).exists():
            i += 1
            username = u'{0}{1}'.format(details['username'], i);
        final_username = username
    else:
        final_username = user.username
    return {'username': final_username}
