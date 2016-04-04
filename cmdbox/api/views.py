from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext as _

from cmdbox.snippets.models import Snippet


def snippet(request, username, slug):
    try:
        _snippet = Snippet.objects.get(user__username=username, slug=slug)
        is_help_request = 'h' in request.GET or 'help' in request.GET

        if is_help_request:
            return HttpResponse(_snippet.content, content_type='text/plain')
        else:
            format_params = _snippet.get_params()

            get_args = request.GET.get('a', request.GET.get('args', None))
            args = list()
            if get_args is not None:
                args = get_args.split(',')

            kwargs = dict()
            for field_name in format_params['kwargs']:
                if field_name in request.GET:
                    kwargs[field_name] = request.GET.get(field_name)

            try:
                output = _snippet.use(args, kwargs)
                return HttpResponse(output, content_type='text/plain')
            except (ValueError, IndexError, KeyError) as e:
                return HttpResponseBadRequest(e.message, content_type='text/plain')

    except Snippet.DoesNotExist:
        error_message = _('[S01] Invalid URL. The snippet does not exist.')
        return HttpResponseBadRequest(error_message, content_type='text/plain')
