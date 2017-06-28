from contextlib import contextmanager
from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from freezegun import freeze_time


def setup_phase(phase_factory, item_factory, phase_content_class, **kwargs):
    phase_content = phase_content_class()
    phase = phase_factory(phase_content=phase_content, **kwargs)
    module = phase.module
    project = phase.module.project
    item = item_factory(module=module) if item_factory else None
    return phase, module, project, item


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
