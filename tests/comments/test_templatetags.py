import html
import json
import re

import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from freezegun import freeze_time

from adhocracy4.comments.serializers import ThreadSerializer
from adhocracy4.test import helpers


def react_comment_render_for_props(rf, user, question):
    request = rf.get('/')
    request.user = user
    template = '{% load react_comments %}{% react_comments question %}'
    context = {'request': request, "question": question}

    content_type = ContentType.objects.get_for_model(question)
    expected = (
        r'^<div data-a4-widget=\"comment\" data-attributes='
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

        comments = ThreadSerializer(
            question.comments.all().order_by('-created'),
            many=True, context={'request': request}).data

        assert props == {
            'comments': comments,
            'comments_contenttype': comments_content_type.pk,
            'isAuthenticated': False,
            'isModerator': False,
            'isReadOnly': True,
            'user_name': '',
            'isContextMember': True,
        }


@pytest.mark.django_db
def test_react_rating_user(rf, user, phase, question, comment):
    with freeze_time('2013-01-02 18:00:00 UTC'):
        props = react_comment_render_for_props(rf, user, question)
        comments_content_type = ContentType.objects.get_for_model(comment)
        request = rf.get('/')
        request.user = user

        comments = ThreadSerializer(
            question.comments.all().order_by('-created'),
            many=True, context={'request': request}).data

        assert props == {
            'comments': comments,
            'comments_contenttype': comments_content_type.pk,
            'isAuthenticated': True,
            'isModerator': False,
            'isReadOnly': False,
            'user_name': user.username,
            'isContextMember': True,
        }
