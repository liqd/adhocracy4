import pytest

from adhocracy4.filters.filters import ClassBasedViewFilterSet
from adhocracy4.filters.views import FilteredListView
from adhocracy4.labels.filters import LabelAliasFilter
from adhocracy4.labels.filters import LabelFilter
from adhocracy4.projects.mixins import ProjectMixin
from tests.apps.ideas.models import Idea


class ExampleFilterSet(ClassBasedViewFilterSet):
    labels = LabelFilter()

    class Meta:
        model = Idea
        fields = ["labels"]


class ExampleAliasFilterSet(ClassBasedViewFilterSet):
    labels = LabelAliasFilter()

    class Meta:
        model = Idea
        fields = ["labels"]


@pytest.fixture
def idea_list_view():
    class DummyView(FilteredListView, ProjectMixin):
        model = Idea
        filter_set = ExampleFilterSet

    return DummyView.as_view()


@pytest.mark.django_db
def test_label_filter_labels(rf, module_factory, label_factory):
    """Check that the right labels are in the view."""
    module = module_factory()
    label1 = label_factory(module=module)
    another_module = module_factory()
    label2 = label_factory(module=another_module)

    class ViewDummy:
        module = another_module

    request = rf.get("/")
    filterset = ExampleFilterSet(request, queryset=Idea.objects.all(), view=ViewDummy())

    filter_queryset = filterset.filters["labels"].get_queryset(request)
    assert list(filter_queryset) == [label2]
    assert label1 not in filter_queryset


@pytest.mark.django_db
def test_label_alias_filter_labels(rf, module_factory, label_factory):
    """Check that the right labels are in the view."""
    module = module_factory()
    label1 = label_factory(module=module)
    another_module = module_factory()
    label2 = label_factory(module=another_module)

    class ViewDummy:
        module = another_module

    request = rf.get("/")
    filterset = ExampleAliasFilterSet(
        request, queryset=Idea.objects.all(), view=ViewDummy()
    )

    filter_queryset = filterset.filters["labels"].get_queryset(request)
    assert list(filter_queryset) == [label2]
    assert label1 not in filter_queryset


@pytest.mark.django_db
def test_label_filter(rf, idea_list_view, label_factory, idea_factory):
    label1 = label_factory()
    label2 = label_factory(module=label1.module)
    idea1 = idea_factory.create(labels=(label1, label2))
    idea1.save()
    idea2 = idea_factory.create(labels=(label1,))
    idea2.save()

    module = label1.module

    request = rf.get("/ideas")
    response = idea_list_view(request, module=module)
    idea_list = response.context_data["idea_list"]
    assert len(idea_list) == 2

    request = rf.get("/ideas?labels=")
    response = idea_list_view(request, module=module)
    idea_list = response.context_data["idea_list"]
    assert len(idea_list) == 2

    request = rf.get("/ideas?labels={}".format(label1.pk))
    response = idea_list_view(request, module=module)
    idea_list = response.context_data["idea_list"]
    assert len(idea_list) == 2

    request = rf.get("/ideas?labels={}".format(label2.pk))
    response = idea_list_view(request, module=module)
    idea_list = response.context_data["idea_list"]
    assert len(idea_list) == 1

    request = rf.get("/ideas?labels=katze")
    response = idea_list_view(request, module=module)
    idea_list = response.context_data["idea_list"]
    assert len(idea_list) == 2
