import pytest
from django.urls import reverse

from adhocracy4.dashboard import components


@pytest.mark.django_db
def test_ideas_export_component(module_factory):
    module_idea_collection = module_factory(blueprint_type="IC")
    module_text_review = module_factory(blueprint_type="TR")
    component = components.modules.get("idea_export")

    assert component.is_effective(module_idea_collection)
    assert not component.is_effective(module_text_review)

    assert component.get_progress(module_idea_collection) == (0, 0)

    assert component.get_base_url(module_idea_collection) == reverse(
        "a4dashboard:idea-export-module",
        kwargs={"module_slug": module_idea_collection.slug},
    )
