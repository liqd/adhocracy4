import pytest
from dateutil.parser import parse

from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.filters.filters import DynamicChoicesOrderingFilter
from adhocracy4.filters.views import FilteredListView
from tests.apps.questions import models as question_models


class ExampleDefaultsFilterSet(DefaultsFilterSet):
    defaults = {
        'ordering': '-created'
    }
    ordering = DynamicChoicesOrderingFilter(
        choices=(('-positive_rating_count', 'Most popular'),
                 ('-comment_count', 'Most commented'),
                 ('-created', 'Most recent'))

    )

    class Meta:
        model = question_models.Question
        fields = ['ordering']


@pytest.fixture
def question_list_view():
    class DummyView(FilteredListView):
        model = question_models.Question
        filter_set = ExampleDefaultsFilterSet
    return DummyView.as_view()


@pytest.mark.django_db
def test_ordering_filter_default(rf, question_list_view, project,
                                 question_factory, comment_factory):
    q1 = question_factory(created=parse('2018-01-01 7:00:00 UTC'))
    q2 = question_factory(created=parse('2019-01-01 7:00:00 UTC'))
    q3 = question_factory(created=parse('2020-01-01 7:00:00 UTC'))
    q4 = question_factory(created=parse('2021-01-01 7:00:00 UTC'))
    comment_factory(content_object=q1)
    comment_factory(content_object=q2)
    comment_factory(content_object=q2)
    comment_factory(content_object=q3)

    request = rf.get('/questions')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert question_list[0] == q4
    assert question_list[1] == q3
    assert question_list[2] == q2
    assert question_list[3] == q1

    request = rf.get('/questions?ordering=')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert question_list[0] == q1
    assert question_list[1] == q2
    assert question_list[2] == q3
    assert question_list[3] == q4

    request = rf.get('/questions?ordering=invalid_choice')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert question_list[0] == q4
    assert question_list[1] == q3
    assert question_list[2] == q2
    assert question_list[3] == q1

    request = rf.get('/questions?ordering=-comment_count')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert question_list[0] == q2
    assert question_list[1] == q1
    assert question_list[2] == q3
    assert question_list[3] == q4
