import pytest
from django.core.urlresolvers import reverse


@pytest.mark.django_db
def test_adding_participant(client, project, user):
    initiator = project.organisation.initiators.first()
    project.participants.clear()
    client.login(username=initiator.email, password='password')
    url = reverse('dashboard-project-participants', kwargs={
        'slug': project.slug
    })
    response = client.get(url)
    assert response.status_code == 200

    response_form = client.post(url, {
        'add_users': user.email,
    })
    assert response_form.status_code == 302
    assert project.participants.filter(id=user.id).exists()


@pytest.mark.django_db
def test_removing_participant(client, project, user):
    project.participants.add(user)

    initiator = project.organisation.initiators.first()
    client.login(username=initiator.email, password='password')
    url = reverse('dashboard-project-participants', kwargs={
        'slug': project.slug
    })
    response = client.get(url)
    assert response.status_code == 200

    old_count = project.participants.count()

    response_form = client.post(url, {
        'submit_action': 'remove_user',
        'user_pk': user.pk
    })
    assert response_form.status_code == 302
    assert project.participants.count() == old_count - 1
    assert not project.participants.filter(id=user.id).exists()


@pytest.mark.django_db
def test_adding_moderator(client, project, user):
    initiator = project.organisation.initiators.first()
    project.moderators.clear()
    client.login(username=initiator.email, password='password')
    url = reverse('dashboard-project-moderators', kwargs={
        'slug': project.slug
    })
    response = client.get(url)
    assert response.status_code == 200

    response_form = client.post(url, {
        'add_users': user.email,
    })
    assert response_form.status_code == 302
    assert project.moderators.filter(id=user.id).exists()


@pytest.mark.django_db
def test_removing_moderator(client, project):
    initiator = project.organisation.initiators.first()
    mod = project.moderators.first()
    client.login(username=initiator.email, password='password')
    url = reverse('dashboard-project-moderators', kwargs={
        'slug': project.slug
    })
    response = client.get(url)
    assert response.status_code == 200

    old_count = project.moderators.count()

    response_form = client.post(url, {
        'submit_action': 'remove_user',
        'user_pk': mod.pk
    })
    assert response_form.status_code == 302
    assert project.moderators.count() == old_count - 1
    assert not project.moderators.filter(id=mod.id).exists()
