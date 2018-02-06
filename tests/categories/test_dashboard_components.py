import pytest

from adhocracy4.categories.dashboard import ModuleCategoriesComponent


@pytest.mark.django_db
def test_module_categories_settings(phase):
    # Note: this test depends on tests.project.settings.A4_CATEGORIZABLE
    component = ModuleCategoriesComponent()
    assert component.is_effective(phase.module) is True
