import importlib
import json
import os
from contextlib import contextmanager
from unittest import mock
from urllib.parse import urlparse

from django.conf import settings
from django.core.urlresolvers import resolve
from django.template import Context, Template
from easy_thumbnails.files import get_thumbnailer


def create_thumbnail(imagefield):
    thumbnailer = get_thumbnailer(imagefield)
    thumbnail = thumbnailer.generate_thumbnail(
        {'size': (800, 400), 'crop': 'smart'})
    thumbnailer.save_thumbnail(thumbnail)
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, thumbnail.path)
    return thumbnail_path


def templates_used(response):
    if not hasattr(response, 'templates'):
        raise Exception("Response wasn't render from template")
    names = [template.name for template in response.templates]
    return names


def redirect_target(response):
    if response.status_code not in [301, 302]:
        raise Exception("Response wasn't a redirect")
    location = urlparse(response['location'])
    return resolve(location.path).url_name


def render_template(string, context=None):
    context = Context(context or {})
    return Template(string).render(context)


@contextmanager
def skip_background_mail():
    def skip_background_decorator(*args, **kwargs):
        # ignore args and kwargs as they are arguments for background tasks
        def send_sync_decorator(fun):
            def send_sync_checked(*args, **kwargs):
                # Ensure the arguments are json serializable
                json.dumps((args, kwargs))
                return fun(*args, **kwargs)
            return send_sync_checked
        return send_sync_decorator

    decorator = 'background_task.background'
    decorated_module = 'adhocracy4.emails.tasks'

    module = importlib.import_module(decorated_module)

    # Patch the decorator and reload the module
    with mock.patch(decorator, wraps=skip_background_decorator):
        importlib.reload(module)
        yield

    # Reset the decorator by reloading the module
    importlib.reload(module)
