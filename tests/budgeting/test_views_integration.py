import pytest
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.budgeting import models
from meinberlin.apps.budgeting import phases
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import setup_phase


@pytest.mark.django_db
def test_list_view(client, phase_factory, proposal_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_budgeting/proposal_list.html')


@pytest.mark.django_db
def test_detail_view(client, phase_factory, proposal_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    url = item.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_budgeting/proposal_detail.html')


@pytest.mark.django_db
def test_create_view(client, phase_factory, proposal_factory, user,
                     category_factory, area_settings_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    area_settings_factory(module=module)
    category = category_factory(module=module)
    url = reverse('meinberlin_budgeting:proposal-create',
                  kwargs={'module_slug': module.slug})
    with freeze_phase(phase):
        client.login(username=user.email, password='password')

        response = client.get(url)
        assert_template_response(
            response,
            'meinberlin_budgeting/proposal_create_form.html')

        data = {
            'name': 'Idea',
            'description': 'description',
            'category': category.pk,
            'budget': 123,
            'point': (0, 0),
            'point_label': 'somewhere',
            'allow_contact': False,
        }
        response = client.post(url, data)
        assert redirect_target(response) == 'proposal-detail'


@pytest.mark.django_db
def test_update_view(client, phase_factory, proposal_factory, user,
                     category_factory, area_settings_factory):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    area_settings_factory(module=module)
    category = category_factory(module=module)
    url = reverse('meinberlin_budgeting:proposal-update',
                  kwargs={'pk': '{:05d}'.format(proposal.pk),
                          'year': proposal.created.year})
    with freeze_phase(phase):
        client.login(username=user.email, password='password')
        response = client.get(url)
        assert response.status_code == 403

        client.login(username=proposal.creator.email, password='password')
        response = client.get(url)
        assert_template_response(
            response,
            'meinberlin_budgeting/proposal_update_form.html')

        data = {
            'name': 'Idea',
            'description': 'super new description',
            'category': category.pk,
            'budget': 123,
            'point': (0, 0),
            'point_label': 'somewhere',
            'allow_contact': False,
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert redirect_target(response) == 'proposal-detail'
        updated_proposal = models.Proposal.objects.get(id=proposal.pk)
        assert updated_proposal.description == 'super new description'


@pytest.mark.django_db
def test_moderate_view(client, phase_factory, proposal_factory, user,
                       area_settings_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    area_settings_factory(module=module)
    url = reverse('meinberlin_budgeting:proposal-moderate',
                  kwargs={'pk': item.pk, 'year': item.created.year})
    project.moderators.set([user])
    with freeze_phase(phase):
        client.login(username=user.email, password='password')

        response = client.get(url)
        assert_template_response(
            response,
            'meinberlin_budgeting/proposal_moderate_form.html')

        data = {
            'moderator_feedback': 'test',
            'is_archived': False,
            'statement': 'its a statement'
        }
        response = client.post(url, data)
        assert redirect_target(response) == 'proposal-detail'


@pytest.mark.django_db
def test_export_view(client, proposal_factory, module_factory):
    proposal = proposal_factory()
    organisation = proposal.module.project.organisation
    initiator = organisation.initiators.first()
    client.login(username=initiator.email, password='password')
    url = reverse('a4dashboard:budgeting-export',
                  kwargs={'module_slug': proposal.module.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert (response._headers['content-type'] ==
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.'
            'spreadsheetml.sheet'))
