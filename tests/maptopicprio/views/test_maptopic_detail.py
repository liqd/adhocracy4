import pytest

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.maptopicprio import phases
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import setup_phase


@pytest.mark.django_db
def test_detail_view(client, phase_factory, maptopic_factory):
    phase, module, project, maptopic = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase)
    url = maptopic.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_maptopicprio/maptopic_detail.html')
        assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_private_not_visible_anonymous(client,
                                                   phase_factory,
                                                   maptopic_factory):
    phase, module, project, maptopic = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase)
    maptopic.module.project.access = Access.PRIVATE
    maptopic.module.project.save()
    url = maptopic.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'


@pytest.mark.django_db
def test_detail_view_private_not_visible_normal_user(client,
                                                     user,
                                                     phase_factory,
                                                     maptopic_factory):
    phase, module, project, maptopic = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase)
    maptopic.module.project.access = Access.PRIVATE
    maptopic.module.project.save()
    assert user not in maptopic.module.project.participants.all()
    client.login(username=user.email,
                 password='password')
    url = maptopic.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_detail_view_private_visible_to_participant(client,
                                                    user,
                                                    phase_factory,
                                                    maptopic_factory):
    phase, module, project, maptopic = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase)
    maptopic.module.project.access = Access.PRIVATE
    maptopic.module.project.save()
    url = maptopic.get_absolute_url()
    assert user not in maptopic.module.project.participants.all()
    maptopic.module.project.participants.add(user)
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_private_visible_to_moderator(client,
                                                  phase_factory,
                                                  maptopic_factory):
    phase, module, project, maptopic = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase)
    maptopic.module.project.access = Access.PRIVATE
    maptopic.module.project.save()
    url = maptopic.get_absolute_url()
    user = maptopic.project.moderators.first()
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_private_visible_to_initiator(client,
                                                  phase_factory,
                                                  maptopic_factory):
    phase, module, project, maptopic = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase)
    maptopic.module.project.access = Access.PRIVATE
    maptopic.module.project.save()
    url = maptopic.get_absolute_url()
    user = maptopic.project.organisation.initiators.first()
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200
