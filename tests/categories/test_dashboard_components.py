import pytest

from adhocracy4.categories.dashboard import ModuleCategoriesComponent


@pytest.mark.django_db
def test_module_categories_settings(phase_factory):
    # Note: this test depends on tests.project.settings.A4_CATEGORIZABLE
    phase = phase_factory(type="a4test_questions:ask")
    component = ModuleCategoriesComponent()
    assert component.is_effective(phase.module) is True
