import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_container_list_view(
        project_container_factory, project_factory,
        organisation, client):
    container_1 = project_container_factory(organisation=organisation)
    container_2 = project_container_factory(organisation=organisation)
    container_3 = project_container_factory()
    assert container_3.organisation != organisation
    project = project_factory(organisation=organisation)
    assert project.organisation == organisation
    initiator = organisation.initiators.first()
    url = reverse('a4dashboard:container-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert container_1 in response.context_data['projectcontainer_list']
    assert container_2 in response.context_data['projectcontainer_list']
    assert container_3 not in response.context_data['projectcontainer_list']
    assert project not in response.context_data['projectcontainer_list']


@pytest.mark.django_db
def test_dashboard_container_list_view_user(user, organisation,
                                            client):
    assert user not in organisation.initiators.all()
    url = reverse('a4dashboard:container-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=user.email, password='password')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_dashboard_container_list_view_group_member(
        project_container_factory, project_factory, organisation, client,
        user_factory, group_factory):
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1, ))
    organisation.groups.add(group1)
    container_1 = project_container_factory(organisation=organisation)
    container_1.group = group1
    container_1.save()
    container_2 = project_container_factory(organisation=organisation)
    container_3 = project_container_factory()
    assert container_3.organisation != organisation
    project = project_factory(organisation=organisation)
    project.group = group1
    project.save()
    assert project.organisation == organisation
    url = reverse('a4dashboard:container-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=group_member.email, password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert container_1 in response.context_data['projectcontainer_list']
    assert container_2 not in response.context_data['projectcontainer_list']
    assert container_3 not in response.context_data['projectcontainer_list']
    assert project not in response.context_data['projectcontainer_list']
