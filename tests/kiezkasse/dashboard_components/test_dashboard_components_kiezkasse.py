import pytest
from django.urls import reverse

from adhocracy4.dashboard import components


@pytest.mark.django_db
def test_kiezkasse_export_component(module_factory):
    module_kiezkasse = module_factory(blueprint_type='KK')
    module_idea_collection = module_factory(blueprint_type='IC')
    component = components.modules.get('kiezkasse_export')

    assert component.is_effective(module_kiezkasse)
    assert not component.is_effective(module_idea_collection)

    assert component.get_progress(module_kiezkasse) == (0, 0)

    assert component.get_base_url(module_kiezkasse) == \
           reverse('a4dashboard:kiezkasse-export-module',
                   kwargs={'module_slug': module_kiezkasse.slug})
