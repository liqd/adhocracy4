import pytest

from adhocracy4.labels.dashboard import ModuleLabelsComponent


@pytest.mark.django_db
def test_module_categories_settings(phase_factory):
    # Note: this test depends on tests.project.settings.A4_LABELS_ADDABLE
    phase = phase_factory(type="a4test_questions:ask")
    component = ModuleLabelsComponent()
    assert component.is_effective(phase.module) is True
