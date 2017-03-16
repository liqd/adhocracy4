import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_get_class_running_out(question, phase):
    question.module = phase.module
    template = '{% load module_tags %}' \
               '{% if item|has_feature:"crud" %}True{% endif %}'
    assert 'True' == render_template(template, {'item': question})
