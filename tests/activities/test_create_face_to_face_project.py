import pytest
from django.urls import reverse

from meinberlin.test.helpers import setup_users


@pytest.mark.django_db
def test_facetoface_in_blueprints(client, project):
    anonymous, moderator, initiator = setup_users(project)
    client.login(username=initiator.email, password='password')
    blueprints_url = reverse(
        'a4dashboard:blueprint-list',
        kwargs={
            'organisation_slug': project.organisation.slug
        })
    facetoface_blueprint_url = reverse(
        'a4dashboard:project-create',
        kwargs={
            'blueprint_slug': 'facetoface',
            'organisation_slug': project.organisation.slug
        })
    resp = client.get(blueprints_url, follow=True)
    assert resp.status_code == 200
    assert facetoface_blueprint_url in resp.content.decode()


@pytest.mark.django_db
def test_xxxx(client, project):
    pass
