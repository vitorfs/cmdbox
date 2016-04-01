from string import Formatter
import pyparsing

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from cmdbox.snippets.models import Snippet


def _count_format_args(format_string):
    formatter = Formatter()
    format_iterator = formatter.parse(format_string)
    named_args = set()
    for _tuple in format_iterator:
        arg = _tuple[1]
        if arg is not None:
            named_args.add(arg)
    print named_args
    return len(named_args)


def _remove_comments(format_string):
    comment = pyparsing.nestedExpr("/*", "*/").suppress()
    output = comment.transformString(format_string)
    return output


def snippet(request, username, slug):
    try:
        _snippet = Snippet.objects.get(user__username=username, slug=slug)

        path = request.get_full_path()
        format_string = _snippet.content
        params_count = _count_format_args(format_string)

        help_request = ('h' or 'help' in request.GET)

        if help_request:
            output = format_string
        else:
            has_format_param = params_count > 0

            has_qs = '?' in path
            qs_param = list()
            if has_qs:
                str_qs_param = path.split('?')[1]
                if len(str_qs_param) > 0:
                    qs_param = str_qs_param.split(',')

            output = ''

            if has_format_param:
                if not len(qs_param):
                    output = format_string  # help content
                elif qs_param:
                    if len(qs_param) == params_count:
                        output = format_string.format(*qs_param)
                    else:
                        return HttpResponseBadRequest('Invalid number of arguments.')
            else:
                if has_qs:
                    output = format_string
                else:
                    output = _remove_comments(format_string)  # help content

        return HttpResponse(output, content_type='text/plain')
    except Snippet.DoesNotExist:
        return HttpResponseBadRequest('Invalid URL. The snippet does not exist.')
    return render(request, 'api/snippet.html')
