import json
import os
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


def patch_background_task_decorator():
    """Patch the 'background' decorator from background_task.

    The decorator will be patched by a synchronous function that
    first checks if its input is json serializable (a prerequisite of
    background_tasks) and second calls the actual task function.
    """
    decorator = 'background_task.background'

    def decorator_mock(*args, **kwargs):
        def background_mock(task_function):
            def json_checked_function(*args, **kwargs):
                # Ensure the arguments are json serializable
                json.dumps((args, kwargs))
                return task_function(*args, **kwargs)
            return json_checked_function
        return background_mock

    patcher = mock.patch(decorator, wraps=decorator_mock)
    return patcher
