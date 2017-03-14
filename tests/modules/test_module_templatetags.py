import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_get_class_running_out(question, phase):
    question.module = phase.module
    template = '{% load module_tags %}' \
               '{% itemHasFeature item "crud" as x %}{{x}}'
    assert 'True' == render_template(template, {'item': question})
