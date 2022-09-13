import pytest
from django.urls import reverse

from adhocracy4.dashboard import components


@pytest.mark.django_db
def test_maptopic_edit_component(module_factory, area_settings,
                                 maptopic_factory):
    module_maptopic_prio = module_factory(blueprint_type='MTP')
    module_maptopic_prio.settings_instance = area_settings
    module_idea_collection = module_factory(blueprint_type='IC')
    component = components.modules.get('map_topic_edit')

    assert component.is_effective(module_maptopic_prio)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_maptopic_prio) == (0, 1)
    maptopic_factory(module=module_maptopic_prio)
    assert component.get_progress(module_maptopic_prio) == (1, 1)

    assert component.get_base_url(module_maptopic_prio) == \
           reverse('a4dashboard:maptopic-list',
                   kwargs={'module_slug': module_maptopic_prio.slug})


@pytest.mark.django_db
def test_maptopic_export_component(module_factory):
    module_maptopic_prio = module_factory(blueprint_type='MTP')
    module_idea_collection = module_factory(blueprint_type='IC')
    component = components.modules.get('maptopic_export')

    assert component.is_effective(module_maptopic_prio)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_maptopic_prio) == (0, 0)

    assert component.get_base_url(module_maptopic_prio) == \
           reverse('a4dashboard:maptopic-export-module',
                   kwargs={'module_slug': module_maptopic_prio.slug})
