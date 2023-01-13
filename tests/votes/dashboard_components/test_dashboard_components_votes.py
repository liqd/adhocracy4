import pytest
from django.urls import reverse

from adhocracy4.dashboard import components


@pytest.mark.django_db
def test_votes_component(module_factory):
    module_pb3 = module_factory(blueprint_type="PB3")
    module_idea_collection = module_factory(blueprint_type="IC")
    component = components.modules.get("voting_token_export")

    assert component.is_effective(module_pb3)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_pb3) == (0, 0)

    assert component.get_base_url(module_pb3) == reverse(
        "a4dashboard:voting-tokens", kwargs={"module_slug": module_pb3.slug}
    )


@pytest.mark.django_db
def test_votes_generate_votes_component(module_factory):
    module_pb3 = module_factory(blueprint_type="PB3")
    module_idea_collection = module_factory(blueprint_type="IC")
    component = components.modules.get("voting_token_generation")

    assert component.is_effective(module_pb3)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_pb3) == (0, 0)

    assert component.get_base_url(module_pb3) == reverse(
        "a4dashboard:voting-token-generation", kwargs={"module_slug": module_pb3.slug}
    )
