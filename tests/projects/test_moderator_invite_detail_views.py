import pytest
from django.core import mail
from django.urls import reverse

from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.projects.models import ModeratorInvite


@pytest.mark.django_db
def test_user_can_accept(client, moderator_invite, user):
    url = moderator_invite.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 200
    assert response.template_name[0] == \
        'meinberlin_projects/moderatorinvite_detail.html'

    client.login(username=user.email, password='password')
    response = client.get(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'project-moderator-invite-update'
    assert ModeratorInvite.objects.all().count() == 1
    assert str(ModeratorInvite.objects.first()) == \
        'Moderation invite to {} for {}'.format(
            moderator_invite.project, moderator_invite.email)

    data = {
        'accept': ''
    }

    url = reverse(
        'project-moderator-invite-update',
        kwargs={'invite_token': moderator_invite.token})

    response = client.post(url, data)
    assert response.status_code == 302
    assert redirect_target(response) == 'project-detail'
    assert len(mail.outbox) == 0
    assert ModeratorInvite.objects.all().count() == 0


@pytest.mark.django_db
def test_user_can_reject(client, moderator_invite, user):
    client.login(username=user.email, password='password')
    data = {
        'reject': ''
    }

    url = reverse(
        'project-moderator-invite-update',
        kwargs={'invite_token': moderator_invite.token})

    response = client.post(url, data)
    assert response.status_code == 302
    assert redirect_target(response) == 'wagtail_serve'
    assert len(mail.outbox) == 0
    assert ModeratorInvite.objects.all().count() == 0
