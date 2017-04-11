import pytest
from django.core.urlresolvers import reverse


@pytest.mark.django_db
def test_email_regex(client, project):
    user = project.organisation.initiators.first()
    client.login(username=user.email, password='password')
    url = reverse('dashboard-project-moderators', kwargs={
        'organisation_slug': project.organisation.slug,
        'slug': project.slug
    })
    response = client.get(url)
    assert response.status_code == 200

    response_form = client.post(url, {
        'add_moderators': 'max@sdg.de, nina@dsgo.de,peter@qwrde',
    })
    assert 'add_moderators' in response_form.context["form"].errors


@pytest.mark.django_db
def test_adding_moderator(client, project, user):
    initiator = project.organisation.initiators.first()
    project.moderators.clear()
    client.login(username=initiator.email, password='password')
    url = reverse('dashboard-project-moderators', kwargs={
        'organisation_slug': project.organisation.slug,
        'slug': project.slug
    })
    response = client.get(url)
    assert response.status_code == 200

    response_form = client.post(url, {
        'add_moderators': 'max@sdg.de, nina@dsgo.de, {}'.format(user.email),
    })
    assert response_form.status_code == 302
    assert project.moderators.count() == 1
    assert project.moderators.filter(email=user.email).exists()


@pytest.mark.django_db
def test_removing_moderator(client, project):
    initiator = project.organisation.initiators.first()
    mod = project.moderators.first()
    client.login(username=initiator.email, password='password')
    url = reverse('dashboard-project-moderators', kwargs={
        'organisation_slug': project.organisation.slug,
        'slug': project.slug
    })
    response = client.get(url)
    assert response.status_code == 200

    old_count = project.moderators.count()

    response_form = client.post(url, {
        'submit_action': 'remove_moderator',
        'moderator_pk': mod.pk
    })
    assert response_form.status_code == 302
    assert project.moderators.count() == old_count - 1
    assert not project.moderators.filter(email=mod.email).exists()
