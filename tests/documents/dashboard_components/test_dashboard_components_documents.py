import pytest
from django.urls import reverse

from adhocracy4.dashboard import components


@pytest.mark.django_db
def test_documents_edit_component(module_factory, chapter_factory):
    module_text_review = module_factory(blueprint_type="TR")
    module_idea_collection = module_factory(blueprint_type="IC")
    component = components.modules.get("document_settings")

    assert component.is_effective(module_text_review)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_text_review) == (0, 1)
    chapter_factory(module=module_text_review)
    assert component.get_progress(module_text_review) == (1, 1)

    assert component.get_base_url(module_text_review) == reverse(
        "a4dashboard:dashboard-document-settings",
        kwargs={"module_slug": module_text_review.slug},
    )


@pytest.mark.django_db
def test_documents_export_component(module_factory):
    module_text_review = module_factory(blueprint_type="TR")
    module_idea_collection = module_factory(blueprint_type="IC")
    component = components.modules.get("document_export")

    assert component.is_effective(module_text_review)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_text_review) == (0, 0)

    assert component.get_base_url(module_text_review) == reverse(
        "a4dashboard:document-export-module",
        kwargs={"module_slug": module_text_review.slug},
    )
