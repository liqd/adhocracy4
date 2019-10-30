import pytest

from adhocracy4.categories.filters import CategoryFilter
from adhocracy4.filters.filters import ClassBasedViewFilterSet
from tests.apps.questions.models import Question


class ExampleFilterSet(ClassBasedViewFilterSet):
    category = CategoryFilter()

    class Meta:
        model = Question
        fields = ['category']


@pytest.mark.django_db
def test_category_filter(rf, module_factory, category_factory):
    """
    Check that the fk-queryset is filter by the module property of the view.
    """
    module = module_factory()
    category1 = category_factory(module=module)
    another_module = module_factory()
    category2 = category_factory(module=another_module)

    class ViewDummy:
        module = another_module

    request = rf.get('/')
    filterset = ExampleFilterSet(
        request,
        queryset=Question.objects.all(),
        view=ViewDummy()
    )

    filter_queryset = filterset.filters['category'].get_queryset(request)
    assert list(filter_queryset) == [category2]
    assert category1 not in filter_queryset
