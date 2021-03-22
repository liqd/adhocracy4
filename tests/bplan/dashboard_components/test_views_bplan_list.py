import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_bplan_list_view(bplan_factory, project_factory,
                                   organisation, client):
    bplan_1 = bplan_factory(organisation=organisation)
    bplan_2 = bplan_factory(organisation=organisation)
    bplan_3 = bplan_factory()
    assert bplan_3.organisation != organisation
    project = project_factory(organisation=organisation)
    assert project.organisation == organisation
    initiator = organisation.initiators.first()
    url = reverse('a4dashboard:bplan-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert bplan_1 in response.context_data['bplan_list']
    assert bplan_2 in response.context_data['bplan_list']
    assert bplan_3 not in response.context_data['bplan_list']
    assert project not in response.context_data['bplan_list']


@pytest.mark.django_db
def test_dashboard_bplan_list_view_user(user, organisation,
                                        client):
    assert user not in organisation.initiators.all()
    url = reverse('a4dashboard:bplan-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=user.email, password='password')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_dashboard_bplan_list_view_group_member(
        bplan_factory, project_factory, organisation, client,
        user_factory, group_factory):
    group1 = group_factory()
    group_member = user_factory.create(groups=(group1, ))
    organisation.groups.add(group1)
    bplan_1 = bplan_factory(organisation=organisation)
    bplan_1.group = group1
    bplan_1.save()
    bplan_2 = bplan_factory(organisation=organisation)
    bplan_3 = bplan_factory()
    assert bplan_3.organisation != organisation
    project = project_factory(organisation=organisation)
    project.group = group1
    project.save()
    assert project.organisation == organisation
    url = reverse('a4dashboard:bplan-list',
                  kwargs={'organisation_slug': organisation.slug})
    client.login(username=group_member.email, password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert bplan_1 in response.context_data['bplan_list']
    # Currently we don't show the project in the list, but it's in the
    # queryset...
    assert bplan_2 in response.context_data['bplan_list']
    assert bplan_3 not in response.context_data['bplan_list']
    assert project not in response.context_data['bplan_list']
