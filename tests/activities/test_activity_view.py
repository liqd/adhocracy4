import pytest
from django.urls import reverse

from adhocracy4.test.helpers import setup_users


@pytest.mark.django_db
def test_facetoface_in_blueprints(client, project):
    anonymous, moderator, initiator = setup_users(project)
    client.login(username=initiator.email, password='password')
    blueprints_url = reverse(
        'a4dashboard:blueprint-list',
        kwargs={
            'organisation_slug': project.organisation.slug
        })
    # facetoface_blueprint_url = reverse(
    #     'a4dashboard:project-create',
    #     kwargs={
    #         'blueprint_slug': 'facetoface',
    #         'organisation_slug': project.organisation.slug
    #     })
    resp = client.get(blueprints_url, follow=True)
    assert resp.status_code == 200
    # assert facetoface_blueprint_url in resp.content.decode()


@pytest.mark.django_db
def test_create_activity_in_dashboard(user, client, activity_factory,
                                      phase_factory):
    activity = activity_factory()
    phase_factory(module=activity.module)
    anonymous, moderator, initiator = setup_users(activity.project)
    client.login(username=initiator.email, password='password')
    url = reverse(
        'a4dashboard:activities-dashboard',
        kwargs={
            'module_slug': activity.module.slug
        })
    # get the page
    resp = client.get(url)
    assert resp.status_code == 200

    # post invalid data
    resp = client.post(url)
    assert not resp.context['form'].is_valid()

    # post valid data
    resp = client.post(url, {
        'name': 'myname',
        'highlight': 'myhilight',
        'description': 'mydescription'
    })
    assert resp.status_code == 302  # use this an an indicator for success
