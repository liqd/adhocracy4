from collections import OrderedDict

import pytest

from adhocracy4.exports.mixins import ExportModelFieldsMixin
from tests.apps.ideas.models import Idea


@pytest.mark.django_db
def test_model_fields_mixin(idea):
    class Mixin(ExportModelFieldsMixin):
        model = Idea
        fields = ["description", "name"]
        html_fields = ["description"]

    mixin = Mixin()

    virtual = mixin.get_virtual_fields(OrderedDict())
    assert list(virtual.items()) == [("description", "Description"), ("name", "name")]

    idea.description = (
        "&nbsp; &amp;&euro;&lt;&quot;&auml;&ouml;&uuml;" "&#x1F4A9;&nbsp; "
    )
    assert mixin.get_description_data(idea) == '&€<"äöü💩'


@pytest.mark.django_db
def test_model_fields_mixin_exclude(idea):
    class Mixin(ExportModelFieldsMixin):
        model = Idea
        exclude = [
            "moderator_status",
            "moderator_feedback_text",
            "point",
            "point_label",
            "is_bool_test",
        ]

    mixin = Mixin()

    virtual = mixin.get_virtual_fields({})

    assert sorted(virtual.keys()) == [
        "category",
        "created",
        "creator",
        "description",
        "id",
        "labels",
        "modified",
        "module",
        "name",
    ]


@pytest.mark.django_db
def test_model_fields_mixin_related_fields(idea):
    class Mixin(ExportModelFieldsMixin):
        model = Idea
        fields = ["name", "module"]
        related_fields = {"module": ["name", "description"]}

    mixin = Mixin()

    virtual = mixin.get_virtual_fields({})

    assert sorted(virtual.keys()) == ["module_description", "module_name", "name"]


@pytest.mark.django_db
def test_model_fields_mixin_choice_fields(idea):
    class Mixin(ExportModelFieldsMixin):
        model = Idea
        fields = ["name", "moderator_status"]
        choice_fields = ["moderator_status"]

    mixin = Mixin()

    virtual = mixin.get_virtual_fields(OrderedDict())
    assert sorted(virtual.keys()) == ["moderator_status", "name"]

    assert mixin.get_moderator_status_data(idea) == idea.get_moderator_status_display()
