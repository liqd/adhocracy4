from datetime import timedelta

import pytest
from freezegun import freeze_time

from tests.helpers import render_template


def test_get_days_tag():
    template = '{% load project_tags %}{% get_days days as x %}{{x}}'

    assert 'a few hours left' == render_template(template, {'days': 0})
    assert '1 day left' == render_template(template, {'days': 1})
    assert '2 days left' == render_template(template, {'days': 2})


@pytest.mark.django_db
def test_get_class_public(phase):
    project = phase.module.project
    template = '{% load project_tags %}{% get_class project as x %}{{x}}'

    with freeze_time(phase.end_date - timedelta(days=5, minutes=1)):
        assert 'public' == render_template(template, {'project': project})


@pytest.mark.django_db
def test_get_class_running_out(phase):
    project = phase.module.project
    template = '{% load project_tags %}{% get_class project as x %}{{x}}'

    with freeze_time(phase.end_date - timedelta(seconds=1)):
        assert 'running-out' == render_template(template, {'project': project})


@pytest.mark.django_db
def test_get_class_finished(phase):
    project = phase.module.project
    template = '{% load project_tags %}{% get_class project as x %}{{x}}'

    with freeze_time(phase.end_date):
        assert 'finished' == render_template(template, {'project': project})


@pytest.mark.parametrize('project__is_public', [False])
@pytest.mark.django_db
def test_get_class_privat(project):
    template = '{% load project_tags %}{% get_class project as x %}{{x}}'
    assert 'private' == render_template(template, {'project': project})
