import pytest
from django.urls import reverse

from adhocracy4.dashboard import components


@pytest.mark.django_db
def test_interactive_event_livestream_component(module_factory):
    module_ie = module_factory(blueprint_type="IE")
    module_idea_collection = module_factory(blueprint_type="IC")
    component = components.modules.get("live_stream")

    assert component.is_effective(module_ie)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_ie) == (0, 0)

    assert component.get_base_url(module_ie) == reverse(
        "a4dashboard:livequestions-livestream", kwargs={"module_slug": module_ie.slug}
    )


@pytest.mark.django_db
def test_interactive_event_affiliations_component(module_factory):
    module_ie = module_factory(blueprint_type="IE")
    module_idea_collection = module_factory(blueprint_type="IC")
    component = components.modules.get("affiliations")

    assert component.is_effective(module_ie)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_ie) == (0, 0)

    assert component.get_base_url(module_ie) == reverse(
        "a4dashboard:dashboard-affiliations-edit",
        kwargs={"module_slug": module_ie.slug},
    )
