from collections import OrderedDict

import pytest

from adhocracy4.exports.mixins import ExportModelFieldsMixin
from tests.apps.ideas.models import Idea


@pytest.mark.django_db
def test_model_fields_mixin(idea):
    class Mixin(ExportModelFieldsMixin):
        model = Idea
        fields = ['description', 'name']
        html_fields = ['description']

    mixin = Mixin()

    virtual = mixin.get_virtual_fields(OrderedDict())
    assert list(virtual.items()) == [
        ('description', 'Description'),
        ('name', 'name')
    ]

    idea.description = '&nbsp; &amp;&euro;&lt;&quot;&auml;&ouml;&uuml;' \
                       '&#x1F4A9;&nbsp; '
    assert mixin.get_description_data(idea) == '&€<"äöü💩'


@pytest.mark.django_db
def test_model_fields_mixin_exclude(idea):
    class Mixin(ExportModelFieldsMixin):
        model = Idea
        exclude = ['moderator_feedback', 'moderator_statement',
                   'point', 'point_label']

    mixin = Mixin()

    virtual = mixin.get_virtual_fields({})

    assert sorted(virtual.keys()) == ['category', 'created', 'creator',
                                      'description', 'id', 'labels',
                                      'modified', 'module', 'name']
