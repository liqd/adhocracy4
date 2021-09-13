import pytest
from django.core import mail
from django.urls import reverse

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.projects.models import ParticipantInvite


@pytest.mark.django_db
def test_user_can_accept(client, participant_invite, user):
    url = participant_invite.get_absolute_url()
    response = client.get(url)
    assert_template_response(
        response, 'meinberlin_projects/participantinvite_detail.html')

    client.login(username=user.email, password='password')
    response = client.get(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'project-participant-invite-update'
    assert ParticipantInvite.objects.all().count() == 1
    assert str(ParticipantInvite.objects.first()) == \
        'Participation invite to {} for {}'.format(
            participant_invite.project, participant_invite.email)

    data = {
        'accept': ''
    }

    url = reverse(
        'project-participant-invite-update',
        kwargs={'invite_token': participant_invite.token})

    response = client.post(url, data)
    assert response.status_code == 302
    assert redirect_target(response) == 'project-detail'
    assert len(mail.outbox) == 0
    assert ParticipantInvite.objects.all().count() == 0


@pytest.mark.django_db
def test_user_can_reject(client, participant_invite, user):
    client.login(username=user.email, password='password')
    data = {
        'reject': ''
    }

    url = reverse(
        'project-participant-invite-update',
        kwargs={'invite_token': participant_invite.token})

    response = client.post(url, data)
    assert response.status_code == 302
    assert redirect_target(response) == 'wagtail_serve'
    assert len(mail.outbox) == 0
    assert ParticipantInvite.objects.all().count() == 0
