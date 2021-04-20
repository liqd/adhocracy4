import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_project_list_view(
        project_factory, bplan_factory, organisation, client):
    project_1 = project_factory(organisation=organisation)
    project_2 = project_factory(organisation=organisation)
    project_3 = project_factory()
    assert project_3.organisation != organisation
    bplan = bplan_factory(organisation=organisation)
    assert bplan.organisation == organisation
    initiator = organisation.initiators.first()
    url = reverse('a4dashboard:project-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert project_1 in response.context_data['project_list']
    assert project_2 in response.context_data['project_list']
    assert project_3 not in response.context_data['project_list']
    assert bplan not in response.context_data['project_list']


@pytest.mark.django_db
def test_dashboard_project_list_view_user(user, organisation,
                                          client):
    assert user not in organisation.initiators.all()
    url = reverse('a4dashboard:project-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=user.email, password='password')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_dashboard_project_list_view_group_member(
        project_factory, bplan_factory, organisation, client,
        user_factory, group_factory):
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1, ))
    organisation.groups.add(group1)
    project_1 = project_factory(organisation=organisation)
    project_1.group = group1
    project_1.save()
    project_2 = project_factory(organisation=organisation)
    project_3 = project_factory()
    assert project_3.organisation != organisation
    bplan = bplan_factory(organisation=organisation)
    bplan.group = group1
    bplan.save()
    assert bplan.organisation == organisation
    url = reverse('a4dashboard:project-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=group_member.email, password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert project_1 in response.context_data['project_list']
    assert project_2 not in response.context_data['project_list']
    assert project_3 not in response.context_data['project_list']
    assert bplan not in response.context_data['project_list']
