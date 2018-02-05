import pytest

from adhocracy4.dashboard.dashboard import ModuleAreaSettingsComponent


@pytest.mark.django_db
def test_module_area_settings(area_settings):
    module = area_settings.module

    component = ModuleAreaSettingsComponent()
    assert component.is_effective(module) is True
    assert component.get_progress(module) == (1, 1)

    area_settings.polygon = {}
    area_settings.save()
    assert component.get_progress(module) == (0, 1)
