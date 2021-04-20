import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_external_project_list_view(
        external_project_factory, project_factory,
        organisation, client):
    external_1 = external_project_factory(organisation=organisation)
    external_2 = external_project_factory(organisation=organisation)
    external_3 = external_project_factory()
    assert external_3.organisation != organisation
    project = project_factory(organisation=organisation)
    assert project.organisation == organisation
    initiator = organisation.initiators.first()
    url = reverse('a4dashboard:extproject-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert external_1 in response.context_data['externalproject_list']
    assert external_2 in response.context_data['externalproject_list']
    assert external_3 not in response.context_data['externalproject_list']
    assert project not in response.context_data['externalproject_list']


@pytest.mark.django_db
def test_dashboard_external_project_list_view_user(user, organisation,
                                                   client):
    assert user not in organisation.initiators.all()
    url = reverse('a4dashboard:extproject-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=user.email, password='password')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_dashboard_external_project_list_view_group_member(
        external_project_factory, project_factory, organisation, client,
        user_factory, group_factory):
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1, ))
    organisation.groups.add(group1)
    external_1 = external_project_factory(organisation=organisation)
    external_1.group = group1
    external_1.save()
    external_2 = external_project_factory(organisation=organisation)
    external_3 = external_project_factory()
    assert external_3.organisation != organisation
    project = project_factory(organisation=organisation)
    project.group = group1
    project.save()
    assert project.organisation == organisation
    url = reverse('a4dashboard:extproject-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=group_member.email, password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert external_1 in response.context_data['externalproject_list']
    assert external_2 not in response.context_data['externalproject_list']
    assert external_3 not in response.context_data['externalproject_list']
    assert project not in response.context_data['externalproject_list']
