import html
import json
import re

import pytest
from django.contrib.contenttypes.models import ContentType

from adhocracy4.test import helpers


def react_reports_render_template(template, rf, question):
    request = rf.get('/')
    template = '{% load react_reports %}' + template
    context = {'request': request, "question": question}

    content_type = ContentType.objects.get_for_model(question)

    mountpoint = 'report_for_{contenttype}_{pk}'.format(
        contenttype=content_type.id,
        pk=question.id
    )
    modal_name = '{mountpoint}_modal'.format(mountpoint=mountpoint)

    expected = (
        r'^<a href=\"#{modal_name}\" data-a4-widget=\"reports\"'
        r' data-attributes=\"(?P<props>{{.+}})\"'
        r' class=\"(?P<class_names>.*)\">(?P<text>.+)</a>$'
    ).format(modal_name=modal_name)

    match = re.match(expected, helpers.render_template(template, context))
    assert match
    assert match.group('props')
    props = json.loads(html.unescape(match.group('props')))
    assert props['contentType'] == content_type.id
    assert props['objectId'] == question.id
    assert props['modalName'] == modal_name
    del props['contentType']
    del props['objectId']
    del props['modalName']

    assert match.group('class_names')
    assert match.group('text')

    return {
        'props': props,
        'class_names': html.unescape(match.group('class_names')),
        'text': html.unescape(match.group('text'))
    }


@pytest.mark.django_db
def test_react_reports(rf, question):
    template = '{% react_reports question text="test" class="fancy class" %}'
    result = react_reports_render_template(template, rf, question)
    assert result['props'] == {}
    assert result['class_names'] == 'fancy class'
    assert result['text'] == 'test'
