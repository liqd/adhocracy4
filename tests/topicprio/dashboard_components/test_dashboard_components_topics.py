import pytest
from django.urls import reverse

from adhocracy4.dashboard import components


@pytest.mark.django_db
def test_topic_edit_component(module_factory, topic_factory):
    module_topic_prio = module_factory(blueprint_type="TP")
    module_idea_collection = module_factory(blueprint_type="IC")
    component = components.modules.get("topic_edit")

    assert component.is_effective(module_topic_prio)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_topic_prio) == (0, 1)
    topic_factory(module=module_topic_prio)
    assert component.get_progress(module_topic_prio) == (1, 1)

    assert component.get_base_url(module_topic_prio) == reverse(
        "a4dashboard:topic-list", kwargs={"module_slug": module_topic_prio.slug}
    )


@pytest.mark.django_db
def test_topic_export_component(module_factory):
    module_topic_prio = module_factory(blueprint_type="TP")
    module_idea_collection = module_factory(blueprint_type="IC")
    component = components.modules.get("topic_export")

    assert component.is_effective(module_topic_prio)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_topic_prio) == (0, 0)

    assert component.get_base_url(module_topic_prio) == reverse(
        "a4dashboard:topic-export-module",
        kwargs={"module_slug": module_topic_prio.slug},
    )
