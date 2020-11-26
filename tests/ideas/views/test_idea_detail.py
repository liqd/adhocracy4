import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.ideas import phases
from meinberlin.test.helpers import assert_template_response
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import setup_phase


@pytest.mark.django_db
def test_detail_view(client, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    url = idea.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_ideas/idea_detail.html')
        assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_private_not_visible_anonymous(client,
                                                   phase_factory,
                                                   idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    idea.module.project.access = Access.PRIVATE
    idea.module.project.save()
    url = idea.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'


@pytest.mark.django_db
def test_detail_view_private_not_visible_normal_user(client,
                                                     user,
                                                     phase_factory,
                                                     idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    idea.module.project.access = Access.PRIVATE
    idea.module.project.save()
    assert user not in idea.module.project.participants.all()
    client.login(username=user.email,
                 password='password')
    url = idea.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_detail_view_private_visible_to_participant(client,
                                                    user,
                                                    phase_factory,
                                                    idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    idea.module.project.access = Access.PRIVATE
    idea.module.project.save()
    url = idea.get_absolute_url()
    assert user not in idea.module.project.participants.all()
    idea.module.project.participants.add(user)
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_private_visible_to_moderator(client,
                                                  phase_factory,
                                                  idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    idea.module.project.access = Access.PRIVATE
    idea.module.project.save()
    url = idea.get_absolute_url()
    user = idea.project.moderators.first()
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_private_visible_to_initiator(client,
                                                  phase_factory,
                                                  idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    idea.module.project.access = Access.PRIVATE
    idea.module.project.save()
    url = idea.get_absolute_url()
    user = idea.project.organisation.initiators.first()
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_semipublic_participation_only_participant(
        client, user, phase_factory, idea_factory):
    phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.FeedbackPhase)
    idea.module.project.access = Access.SEMIPUBLIC
    idea.module.project.save()

    url = idea.get_absolute_url()
    idea_ct = ContentType.objects.get_for_model(type(idea))
    api_url = reverse('comments-list',
                      kwargs={
                          'content_type': idea_ct.pk,
                          'object_pk': idea.pk
                      })
    comment_data = {
        'comment': 'no comment',
    }

    with freeze_phase(phase):
        response = client.get(url)
        assert response.status_code == 200
        assert_template_response(response, 'meinberlin_ideas/idea_detail.html')
        response = client.post(api_url, comment_data, format='json')

        assert response.status_code == 403

        client.login(username=user.email, password='password')

        response = client.get(url)
        assert response.status_code == 200
        assert_template_response(response, 'meinberlin_ideas/idea_detail.html')
        response = client.post(api_url, comment_data, format='json')
        assert response.status_code == 403

        idea.module.project.participants.add(user)

        response = client.get(url)
        assert response.status_code == 200
        assert_template_response(response, 'meinberlin_ideas/idea_detail.html')
        response = client.post(api_url, comment_data, format='json')
        assert response.status_code == 201
