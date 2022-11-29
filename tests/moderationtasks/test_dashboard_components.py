import pytest

from meinberlin.apps.moderationtasks.dashboard import ModerationTasksComponent


@pytest.mark.django_db
def test_module_moderation_tasks_settings(module_factory):
    module_pb1 = module_factory(blueprint_type='PB')
    module_pb3 = module_factory(blueprint_type='PB3')
    module_ic = module_factory(blueprint_type='IC')
    component = ModerationTasksComponent()
    assert component.is_effective(module_pb1) is True
    assert component.is_effective(module_pb3) is True
    assert component.is_effective(module_ic) is False
