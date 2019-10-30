import pytest
from django.contrib.auth.models import AnonymousUser

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_would_have_perm(rf, question):
    request = rf.get('/')
    template = ('{% load discovery_tags %}'
                '{% would_have_perm "a4test_questions.always_allow" '
                'as would_add %}'
                '{% if would_add %}'
                'CALL TO ACTION!'
                '{% endif %}')
    context = {'request': request}

    assert 'CALL TO ACTION!' == render_template(template, context)


@pytest.mark.django_db
def test_has_or_would_have_perm(rf, question, user):
    request = rf.get('/')
    request.user = user
    template = ('{% load discovery_tags %}'
                '{% has_or_would_have_perm "a4test_questions.always_allow" '
                'request.user as would_add %}'
                '{% if would_add %}'
                'CALL TO ACTION!'
                '{% endif %}')
    context = {'request': request}

    assert 'CALL TO ACTION!' == render_template(template, context)

    request.user = AnonymousUser()
    template = ('{% load discovery_tags %}'
                '{% has_or_would_have_perm "a4test_questions.always_allow" '
                'request.user as would_add %}'
                '{% if would_add %}'
                'CALL TO ACTION!'
                '{% endif %}')
    context = {'request': request}

    assert 'CALL TO ACTION!' == render_template(template, context)
