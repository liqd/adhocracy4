import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.maptopicprio import phases


@pytest.mark.django_db
def test_detail_view(client, phase_factory, maptopic_factory):
    phase, module, project, maptopic = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase)
    url = maptopic.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_maptopicprio/maptopic_detail.html')


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
    assert_template_response(
        response, 'meinberlin_maptopicprio/maptopic_detail.html')


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
    assert_template_response(
        response, 'meinberlin_maptopicprio/maptopic_detail.html')


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
    assert_template_response(
        response, 'meinberlin_maptopicprio/maptopic_detail.html')


@pytest.mark.django_db
def test_detail_view_semipublic_participation_only_participant(
        client, user, phase_factory, maptopic_factory):
    phase, module, project, maptopic = setup_phase(
        phase_factory, maptopic_factory, phases.PrioritizePhase)
    maptopic.module.project.access = Access.SEMIPUBLIC
    maptopic.module.project.save()

    url = maptopic.get_absolute_url()
    maptopic_ct = ContentType.objects.get_for_model(type(maptopic))
    api_url = reverse('comments-list',
                      kwargs={
                          'content_type': maptopic_ct.pk,
                          'object_pk': maptopic.pk
                      })
    comment_data = {
        'comment': 'no comment',
    }

    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_maptopicprio/maptopic_detail.html')
        response = client.post(api_url, comment_data, format='json')

        assert response.status_code == 403

        client.login(username=user.email, password='password')

        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_maptopicprio/maptopic_detail.html')
        response = client.post(api_url, comment_data, format='json')
        assert response.status_code == 403

        maptopic.module.project.participants.add(user)

        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_maptopicprio/maptopic_detail.html')
        response = client.post(api_url, comment_data, format='json')
        assert response.status_code == 201
