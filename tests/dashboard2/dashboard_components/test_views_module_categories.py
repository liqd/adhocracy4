import pytest

from adhocracy4.categories.models import Category
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.dashboard2 import components
from meinberlin.apps.ideas.phases import CollectFeedbackPhase
from meinberlin.test.helpers import assert_dashboard_form_component_response
from meinberlin.test.helpers import setup_phase

component = components.modules.get('categories')


@pytest.mark.django_db
def test_edit_view(client, phase_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase)
    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(module)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert_dashboard_form_component_response(response, component)

    data = {
        'category_set-TOTAL_FORMS': 1,
        'category_set-INITIAL_FORMS': 0,
        'category_set-0-id': '',
        'category_set-0-module': module.pk,
        'category_set-0-name': 'test',
    }
    response = client.post(url, data)
    assert redirect_target(response) == \
        'dashboard-{}-edit'.format(component.identifier)
    category = Category.objects.first()
    assert category.name == data.get('category_set-0-name')
