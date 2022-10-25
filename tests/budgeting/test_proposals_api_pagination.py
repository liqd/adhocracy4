import pytest
from django.urls import reverse

from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from meinberlin.apps.budgeting.models import Proposal


@pytest.mark.django_db
def test_proposal_list_mixins(apiclient, phase_factory, proposal_factory):
    phase, module, project, proposal = setup_phase(phase_factory,
                                                   proposal_factory,
                                                   phases.RatingPhase)

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    response = apiclient.get(url)

    # pagination
    assert 'count' in response.data
    assert response.data['count'] == 1
    assert 'page_count' in response.data
    assert response.data['page_count'] == 1


@pytest.mark.django_db
def test_proposal_list_pagination(apiclient, module, proposal_factory):

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})
    response = apiclient.get(url)
    pagesize = response.data['page_size']

    for i in range(pagesize + 1):
        proposal_factory(module=module)

    response = apiclient.get(url)

    assert response.data['count'] == pagesize + 1
    assert response.data['next'].endswith('?page=2')
    assert not response.data['previous']
    assert response.data['page_count'] == 2
    assert len(response.data['results']) == pagesize

    url_tmp = url + '?page=2'
    response = apiclient.get(url_tmp)
    assert not response.data['next']
    assert response.data['previous'].endswith(url)
    assert len(response.data['results']) == 1

    proposal = Proposal.objects.last()
    proposal.is_archived = True
    proposal.save()

    url_tmp = url + '?is_archived=false'
    response = apiclient.get(url_tmp)
    assert not response.data['next']
    assert not response.data['previous']
    assert response.data['page_count'] == 1
    assert len(response.data['results']) == pagesize
