import os
from contextlib import contextmanager
from datetime import timedelta
from urllib.parse import urlparse

import factory
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db.models.signals import post_save
from django.template import Context
from django.template import Template
from django.urls import resolve
from easy_thumbnails.files import get_thumbnailer
from freezegun import freeze_time


def create_thumbnail(imagefield):
    thumbnailer = get_thumbnailer(imagefield)
    thumbnail = thumbnailer.generate_thumbnail({"size": (800, 400), "crop": "smart"})
    thumbnailer.save_thumbnail(thumbnail)
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, thumbnail.path)
    return thumbnail_path


def templates_used(response):
    if not hasattr(response, "templates"):
        raise Exception("Response wasn't render from template")
    names = [template.name for template in response.templates]
    return names


def redirect_target(response):
    if response.status_code not in [301, 302]:
        raise Exception("Response wasn't a redirect")
    location = urlparse(response["location"])
    return resolve(location.path).url_name


def render_template(string, context=None):
    context = Context(context or {})
    return Template(string).render(context)


def dispatch_view(view_class, request, *args, **kwargs):
    """Mimic as_view() and dispatch() but returns view instance in addition."""
    view = view_class()
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view.dispatch(request, *args, **kwargs), view


@factory.django.mute_signals(post_save)
def setup_phase(phase_factory, item_factory, phase_content_class, **kwargs):
    phase_content = phase_content_class()
    phase = phase_factory(phase_content=phase_content, **kwargs)
    module = phase.module
    project = phase.module.project
    item = item_factory(module=module) if item_factory else None
    return phase, module, project, item


@factory.django.mute_signals(post_save)
def setup_users(project):
    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()
    return anonymous, moderator, initiator


@contextmanager
def freeze_phase(phase):
    with freeze_time(phase.start_date + timedelta(seconds=1)):
        yield


@contextmanager
def freeze_pre_phase(phase):
    with freeze_time(phase.start_date - timedelta(seconds=1)):
        yield


@contextmanager
def freeze_post_phase(phase):
    with freeze_time(phase.end_date + timedelta(seconds=1)):
        yield


def assert_template_response(response, template_name, status_code=200):
    assert response.status_code == status_code
    response_template = response.template_name[0]
    assert response_template == template_name, "{} != {}".format(
        response_template, template_name
    )
