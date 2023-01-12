import django_filters
import pytest

from adhocracy4.filters.filters import DynamicChoicesOrderingFilter
from adhocracy4.filters.views import FilteredListView
from adhocracy4.ratings.models import Rating
from tests.apps.questions import models as question_models


def get_ordering_choices(view):
    choices = (
        ("-positive_rating_count", "Most popular"),
        ("-comment_count", "Most commented"),
        ("text", "Alphabetical"),
    )
    return choices


class OrderingFilterSet(django_filters.FilterSet):

    ordering = DynamicChoicesOrderingFilter(choices=get_ordering_choices)

    class Meta:
        model = question_models.Question
        fields = ["ordering"]


@pytest.fixture
def question_list_view():
    class DummyView(FilteredListView):
        model = question_models.Question
        filter_set = OrderingFilterSet

    return DummyView.as_view()


@pytest.mark.django_db
def test_ordering_filter(
    rf, question_list_view, phase, question_factory, comment_factory, rating_factory
):
    project = phase.module.project
    q1 = question_factory(text="zoot")
    q2 = question_factory(text="quark")
    q3 = question_factory(text="park")
    q4 = question_factory(text="or")
    q5 = question_factory(text="alphabet")
    comment_factory(content_object=q2)
    comment_factory(content_object=q3)
    comment_factory(content_object=q3)
    comment_factory(content_object=q4)
    rating_factory(content_object=q2, value=Rating.POSITIVE)
    rating_factory(content_object=q4, value=Rating.POSITIVE)
    rating_factory(content_object=q4, value=Rating.POSITIVE)

    request = rf.get("/questions")
    response = question_list_view(request, project=project)
    question_list = response.context_data["question_list"]
    assert question_list[0] == q1
    assert question_list[1] == q2
    assert question_list[2] == q3
    assert question_list[3] == q4
    assert question_list[4] == q5

    request = rf.get("/questions?ordering=")
    response = question_list_view(request, project=project)
    question_list = response.context_data["question_list"]
    assert question_list[0] == q1
    assert question_list[1] == q2
    assert question_list[2] == q3
    assert question_list[3] == q4
    assert question_list[4] == q5

    request = rf.get("/questions?ordering=text")
    response = question_list_view(request, project=project)
    question_list = response.context_data["question_list"]
    assert question_list[0] == q5
    assert question_list[1] == q4
    assert question_list[2] == q3
    assert question_list[3] == q2
    assert question_list[4] == q1

    request = rf.get("/questions?ordering=-positive_rating_count")
    response = question_list_view(request, project=project)
    question_list = response.context_data["question_list"]
    assert question_list[0] == q4
    assert question_list[1] == q2
    assert question_list[2] == q1
    assert question_list[3] == q3
    assert question_list[4] == q5

    request = rf.get("/questions?ordering=-comment_count")
    response = question_list_view(request, project=project)
    question_list = response.context_data["question_list"]
    assert question_list[0] == q3
    assert question_list[1] == q2
    assert question_list[2] == q4
    assert question_list[3] == q1
    assert question_list[4] == q5
