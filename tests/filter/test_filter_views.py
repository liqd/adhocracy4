import pytest

from tests.apps.questions import models as question_models

from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.modules.views import ItemListView


class TextFilter(DefaultsFilterSet):

    defaults = {
        'text': 'a'
    }

    class Meta:
        model = question_models.Question
        fields = ['text']


@pytest.fixture
def question_list_view():
    class DummyView(ItemListView):
        model = question_models.Question
        filter_set = TextFilter
    return DummyView.as_view()


@pytest.mark.django_db
def test_default_filter(rf, question_list_view, phase, question_factory):
    project = phase.module.project
    request = rf.get('/questions')
    q1 = question_factory()
    q1.text = 'x'
    q1.save()
    q2 = question_factory()
    q2.text = 'a'
    q2.save()
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 1


@pytest.mark.django_db
def test_filter_custom(rf, question_list_view, phase, question_factory):
    project = phase.module.project
    request = rf.get('/questions?text=x')
    q1 = question_factory()
    q1.text = 'x'
    q1.save()
    q2 = question_factory()
    q2.text = 'y'
    q2.save()
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 1


@pytest.mark.django_db
def test_filter_all(rf, question_list_view, phase, question_factory):
    project = phase.module.project
    request = rf.get('/questions?text=')
    q1 = question_factory()
    q1.text = 'x'
    q1.save()
    q2 = question_factory()
    q2.text = 'y'
    q2.save()
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 2
