import pytest

from adhocracy4.filters.filters import ClassBasedViewFilterSet
from adhocracy4.filters.views import FilteredListView
from tests.apps.questions import models as question_models


class ExampleFilterSet(ClassBasedViewFilterSet):
    class Meta:
        model = question_models.Question
        fields = ['text']


@pytest.fixture
def question_list_view():
    class DummyView(FilteredListView):
        model = question_models.Question
        filter_set = ExampleFilterSet
    return DummyView


@pytest.mark.django_db
def test_class_based_filterset(rf):
    class ViewPlaceHolder:
        pass

    view = ViewPlaceHolder
    request = rf.get('/questions')

    filterset = ExampleFilterSet(request.GET, view=view)

    assert filterset.view == view
    assert filterset.filters['text'].view == view


def test_integration_into_filtered_listview(rf, question_list_view):
    request = rf.get('/')
    view = question_list_view.as_view()
    response = view(request)
    view_instance = response.context_data['view']

    assert view_instance.filter().view == view_instance
