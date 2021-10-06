import json
from functools import wraps
from raven.contrib.django.raven_compat.models import client

from django.http import HttpResponseBadRequest, JsonResponse


def sentry_exceptions(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            client.captureMessage(str(e))
            raise

    return inner


def ajax_decorator(a_func):
    @wraps(a_func)
    def decorated_function(request):
        if not request.is_ajax():
            return HttpResponseBadRequest('only ajax allowed')
        return a_func(request)
    return decorated_function


def post_decorator(a_func):
    @wraps(a_func)
    def decorated_function(request):
        if not request.method == 'POST':
            return HttpResponseBadRequest('bad http method')
        return a_func(request)
    return decorated_function


def json_valid_decorator(a_func):
    @wraps(a_func)
    def decorated_function(request):
        try:
            json.loads(request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return JsonResponse({'validated': False, 'text': 'invalid data'})
        return a_func(request)
    return decorated_function
