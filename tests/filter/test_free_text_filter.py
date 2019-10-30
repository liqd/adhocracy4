import django_filters
import pytest
from django.core.exceptions import ImproperlyConfigured

from adhocracy4.filters.filters import FreeTextFilter
from adhocracy4.filters.views import FilteredListView
from tests.apps.questions import models as question_models


class SearchFilterSet(django_filters.FilterSet):

    search = FreeTextFilter(
        fields=['text']
    )

    class Meta:
        model = question_models.Question
        fields = ['search']


@pytest.fixture
def question_list_view():
    class DummyView(FilteredListView):
        model = question_models.Question
        filter_set = SearchFilterSet
    return DummyView.as_view()


@pytest.mark.django_db
def test_free_text_filter(rf, question_list_view, phase, question_factory):
    project = phase.module.project
    question_factory(text='some text')
    question_factory(text='more text')

    request = rf.get('/questions')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 2

    request = rf.get('/questions?search=')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 2

    request = rf.get('/questions?search=text')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 2

    request = rf.get('/questions?search=some')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 1

    request = rf.get('/questions?search=katze')
    response = question_list_view(request, project=project)
    question_list = response.context_data['question_list']
    assert len(question_list) == 0


@pytest.mark.django_db
def test_free_text_filter_exception():
    with pytest.raises(ImproperlyConfigured):
        class SearchFilterSet(django_filters.FilterSet):

            search = FreeTextFilter(
                # no fields set
            )

            class Meta:
                model = question_models.Question
                fields = ['search']
