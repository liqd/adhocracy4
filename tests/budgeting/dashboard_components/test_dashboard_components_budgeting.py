import pytest
from django.urls import reverse

from adhocracy4.dashboard import components


@pytest.mark.django_db
def test_budgeting_export_component(module_factory):
    module_pb = module_factory(blueprint_type="PB")
    module_pb2 = module_factory(blueprint_type="PB2")
    module_pb3 = module_factory(blueprint_type="PB3")
    module_idea_collection = module_factory(blueprint_type="IC")
    component = components.modules.get("budgeting_export")

    assert component.is_effective(module_pb)
    assert component.is_effective(module_pb2)
    assert component.is_effective(module_pb3)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_pb) == (0, 0)

    assert component.get_base_url(module_pb) == reverse(
        "a4dashboard:budgeting-export-module", kwargs={"module_slug": module_pb.slug}
    )
