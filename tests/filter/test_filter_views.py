import pytest

from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.filters.views import FilteredListView
from tests.apps.questions import models as question_models


class TextFilter(DefaultsFilterSet):

    defaults = {
        'text': 'a'
    }

    class Meta:
        model = question_models.Question
        fields = ['text']


@pytest.fixture
def question_list_view():
    class DummyView(FilteredListView):
        model = question_models.Question
        filter_set = TextFilter
    return DummyView.as_view()


@pytest.mark.django_db
def test_default_filter(rf, question_list_view, phase, question_factory):
    project = phase.module.project
    request = rf.get('/questions')
    question_factory(text='x')
    question_factory(text='a')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 1


@pytest.mark.django_db
def test_filter_custom(rf, question_list_view, phase, question_factory):
    project = phase.module.project
    request = rf.get('/questions?text=x')
    question_factory(text='x')
    question_factory(text='y')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 1


@pytest.mark.django_db
def test_filter_all(rf, question_list_view, phase, question_factory):
    project = phase.module.project
    request = rf.get('/questions?text=')
    question_factory(text='x')
    question_factory(text='y')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 2
