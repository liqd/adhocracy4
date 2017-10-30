import pytest

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.bplan import phases
from tests.helpers import freeze_phase


@pytest.mark.django_db
def test_statement_form_view(client, user, phase_factory, bplan,
                             module_factory):
    module = module_factory(project=bplan)
    phase = phase_factory(phase_content=phases.StatementPhase(), module=module)
    url = '/embed' + bplan.get_absolute_url()
    with freeze_phase(phase):
        client.login(username=user.email, password='password')
        statement = {
            'name': 'User',
            'email': 'user@foo.bar',
            'street_number': "Some Street 1",
            'postal_code_city': "12345 City"
        }
        response = client.post(url, statement)
        assert redirect_target(response) == 'idea-detail'
