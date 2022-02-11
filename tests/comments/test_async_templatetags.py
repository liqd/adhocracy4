import html
import json
import re

import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from freezegun import freeze_time

from adhocracy4.test import helpers
from tests.apps.questions.phases import AskPhase


def react_comment_render_for_props(rf, user, question):
    request = rf.get('/')
    request.user = user
    template = ('{% load react_comments_async %}'
                '{% react_comments_async question %}')
    context = {'request': request, "question": question}

    content_type = ContentType.objects.get_for_model(question)
    expected = (
        r'^<div data-a4-widget=\"comment_async\" data-attributes='
        r'\"(?P<props>{.+})\"><\/div>$'
    )

    match = re.match(expected, helpers.render_template(template, context))
    assert match
    assert match.group('props')
    props = json.loads(html.unescape(match.group('props')))
    assert props['subjectType'] == content_type.id
    assert props['subjectId'] == question.id
    del props['subjectType']
    del props['subjectId']
    return props


@pytest.mark.django_db
def test_react_rating_anonymous(rf, question, comment):
    with freeze_time('2013-01-02 18:00:00 UTC'):
        user = AnonymousUser()
        props = react_comment_render_for_props(rf, user, question)
        comments_content_type = ContentType.objects.get_for_model(comment)
        request = rf.get('/')
        request.user = user

        assert props == {
            'comments_contenttype': comments_content_type.pk,
            'isAuthenticated': False,
            'isModerator': False,
            'isReadOnly': True,
            'commentCategoryChoices': {},
            'anchoredCommentId': '',
            'withCategories': False,
            'isContextMember': True,
        }


@pytest.mark.django_db
def test_react_rating_user(rf, user, phase_factory, question_factory,
                           comment):
    phase, _, _, question = helpers.setup_phase(phase_factory,
                                                question_factory,
                                                AskPhase)
    with helpers.freeze_phase(phase):
        props = react_comment_render_for_props(rf, user, question)
        comments_content_type = ContentType.objects.get_for_model(comment)
        request = rf.get('/')
        request.user = user

        assert props == {
            'comments_contenttype': comments_content_type.pk,
            'isAuthenticated': True,
            'isModerator': False,
            'isReadOnly': False,
            'commentCategoryChoices': {},
            'anchoredCommentId': '',
            'withCategories': False,
            'isContextMember': True,
        }


def react_comment_render_for_props_with_categories(rf, user, question):
    request = rf.get('/')
    request.user = user
    template = ('{% load react_comments_async %}'
                '{% react_comments_async question True %}')
    context = {'request': request, "question": question}

    content_type = ContentType.objects.get_for_model(question)
    expected = (
        r'^<div data-a4-widget=\"comment_async\" data-attributes='
        r'\"(?P<props>{.+})\"><\/div>$'
    )

    match = re.match(expected, helpers.render_template(template, context))
    assert match
    assert match.group('props')
    props = json.loads(html.unescape(match.group('props')))
    assert props['subjectType'] == content_type.id
    assert props['subjectId'] == question.id
    del props['subjectType']
    del props['subjectId']
    return props


@pytest.mark.django_db
def test_react_rating_anonymous_with_categories(rf, question, comment):
    with freeze_time('2013-01-02 18:00:00 UTC'):
        user = AnonymousUser()
        props = react_comment_render_for_props_with_categories(rf, user,
                                                               question)
        comments_content_type = ContentType.objects.get_for_model(comment)
        request = rf.get('/')
        request.user = user

        assert props == {
            'comments_contenttype': comments_content_type.pk,
            'isAuthenticated': False,
            'isModerator': False,
            'isReadOnly': True,
            'commentCategoryChoices': {'QUE': 'Question', 'REM': 'Remark'},
            'anchoredCommentId': '',
            'withCategories': True,
            'isContextMember': True,
        }


@pytest.mark.django_db
def test_react_rating_user_with_categories(rf, user, phase_factory,
                                           question_factory,
                                           comment):
    phase, _, _, question = helpers.setup_phase(phase_factory,
                                                question_factory,
                                                AskPhase)
    with helpers.freeze_phase(phase):
        props = react_comment_render_for_props_with_categories(rf, user,
                                                               question)
        comments_content_type = ContentType.objects.get_for_model(comment)
        request = rf.get('/')
        request.user = user

        assert props == {
            'comments_contenttype': comments_content_type.pk,
            'isAuthenticated': True,
            'isModerator': False,
            'isReadOnly': False,
            'commentCategoryChoices': {'QUE': 'Question', 'REM': 'Remark'},
            'anchoredCommentId': '',
            'withCategories': True,
            'isContextMember': True,
        }
