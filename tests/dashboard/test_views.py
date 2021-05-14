import pytest
from django.urls import reverse

from adhocracy4.projects.models import Project
from adhocracy4.test.helpers import redirect_target


@pytest.mark.django_db
def test_project_list(client, organisation,
                      project_factory, user, another_user):
    project0 = project_factory(organisation=organisation)
    project1 = project_factory(organisation=organisation)

    organisation.initiators.add(another_user)

    project_list_url = reverse('a4dashboard:project-list', kwargs={
        'organisation_slug': organisation.slug})
    response = client.get(project_list_url)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(project_list_url)
    assert response.status_code == 403

    client.login(username=another_user, password='password')
    response = client.get(project_list_url)
    assert response.status_code == 200

    project_list = response.context_data['project_list']
    assert list(project_list) == [project1, project0]


@pytest.mark.django_db
def test_blueprint_list(client, organisation, user, another_user):

    blueprint_list_url = reverse('a4dashboard:blueprint-list', kwargs={
        'organisation_slug': organisation.slug})
    response = client.get(blueprint_list_url)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(blueprint_list_url)
    assert response.status_code == 403

    organisation.initiators.add(another_user)
    client.login(username=another_user, password='password')
    response = client.get(blueprint_list_url)
    assert response.status_code == 200

    view = response.context_data['view']
    assert 1 == len(view.blueprints)
    assert 'questions' == view.blueprints[0][0]


@pytest.mark.django_db
def test_project_create(client, organisation, user_factory, group_factory):
    group1 = group_factory()
    group2 = group_factory()
    user = user_factory()
    initiator = user_factory()
    group_member = user_factory.create(groups=(group1, group2))
    organisation.groups.add(group2)

    project_create_url = reverse('a4dashboard:project-create', kwargs={
        'organisation_slug': organisation.slug,
        'blueprint_slug': 'questions'
    })

    data = {
        'name': 'project name',
        'description': 'project description'
    }

    response = client.post(project_create_url, data)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.post(project_create_url, data)
    assert response.status_code == 403

    organisation.initiators.add(initiator)
    client.login(username=initiator, password='password')
    response = client.post(project_create_url, data)
    assert redirect_target(response) == 'project-edit'

    assert 1 == Project.objects.all().count()
    project = Project.objects.all().first()
    assert 'project name' == project.name
    assert 'project description' == project.description

    client.login(username=group_member, password='password')
    response = client.post(project_create_url, data)
    assert redirect_target(response) == 'project-edit'

    assert 2 == Project.objects.all().count()
    assert 1 == Project.objects.filter(group_id=group2.id).count()


@pytest.mark.django_db
def test_project_edit_redirect(client, project):
    project_edit_url = reverse('a4dashboard:project-edit', kwargs={
        'project_slug': project.slug})

    response = client.get(project_edit_url)
    assert response.status_code == 302
    assert response['location'].startswith('/dashboard')


@pytest.mark.django_db
def test_project_publish_perms(client, phase, user, another_user):
    project = phase.module.project

    project_publish_url = reverse('a4dashboard:project-publish', kwargs={
        'project_slug': project.slug})

    data = {'action': 'publish'}

    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.post(project_publish_url, data)
    assert response.status_code == 403

    organisation = project.organisation
    organisation.initiators.add(another_user)
    client.login(username=another_user, password='password')
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'project-edit'


@pytest.mark.django_db
def test_project_publish(client, phase, another_user):
    project = phase.module.project
    project.is_draft = True
    project.information = ''
    project.save()
    organisation = project.organisation
    organisation.initiators.add(another_user)

    project_publish_url = reverse('a4dashboard:project-publish', kwargs={
        'project_slug': project.slug})

    data = {'action': 'publish'}

    # publishing incomplete projects has no effect
    client.login(username=another_user, password='password')
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'project-edit'

    project.refresh_from_db()
    assert project.is_draft is True

    # complete project and publish it
    project.information = 'project information'
    project.save()

    client.login(username=another_user, password='password')
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'project-edit'

    project.refresh_from_db()
    assert project.is_draft is False


@pytest.mark.django_db
def test_project_unpublish(client, phase, another_user):
    project = phase.module.project
    project.is_draft = False
    project.save()
    organisation = project.organisation
    organisation.initiators.add(another_user)

    project_publish_url = reverse('a4dashboard:project-publish', kwargs={
        'project_slug': project.slug})

    data = {'action': 'unpublish'}

    client.login(username=another_user, password='password')
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'project-edit'

    project.refresh_from_db()
    assert project.is_draft is True

    # unpublishing draft projects has no effect
    client.login(username=another_user, password='password')
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'project-edit'

    project.refresh_from_db()
    assert project.is_draft is True


@pytest.mark.django_db
def test_project_publish_redirect(client, project, another_user):
    project_publish_url = reverse('a4dashboard:project-publish', kwargs={
        'project_slug': project.slug})

    organisation = project.organisation
    organisation.initiators.add(another_user)

    client.login(username=another_user, password='password')

    response = client.post(project_publish_url, {'referrer': 'refurl'})
    assert response.status_code == 302
    assert response['location'] == 'refurl'

    response = client.post(project_publish_url, {}, HTTP_REFERER='refurl')
    assert response.status_code == 302
    assert response['location'] == 'refurl'

    response = client.post(project_publish_url, {})
    assert redirect_target(response) == 'project-edit'


@pytest.mark.django_db
def test_project_duplicate(client, another_user,
                           area_settings, phase_factory):
    module = area_settings.module
    project = module.project
    organisation = project.organisation
    organisation.initiators.add(another_user)
    phase = phase_factory(module=module)

    project.is_draft = False
    project.is_archived = True

    project_list_url = reverse('a4dashboard:project-list', kwargs={
        'organisation_slug': organisation.slug})

    client.login(username=another_user, password='password')
    response = client.post(project_list_url, {
        'duplicate': '1',
        'project_pk': project.pk
    })
    assert response.status_code == 302

    assert Project.objects.all().count() == 2

    project_clone = Project.objects.order_by('pk').last()
    assert project_clone.pk != project.pk

    assert project_clone.is_draft is True
    assert project_clone.is_archived is False
    assert project_clone.created > project.created
    for attr in ('description', 'information', 'result', 'access'):
        assert getattr(project_clone, attr) == getattr(project, attr)
    for moderator in project.moderators.all():
        assert moderator in project.moderators.all()

    module_clone = project_clone.module_set.first()
    assert module_clone.pk != module.pk
    for attr in ('name', 'description', 'weight'):
        assert getattr(module_clone, attr) == getattr(module, attr)

    phase_clone = module_clone.phase_set.first()
    assert phase_clone.pk != phase.pk
    for attr in ('name', 'description', 'type', 'start_date', 'end_date',
                 'weight'):
        assert getattr(phase_clone, attr) == getattr(phase, attr)

    area_settings_clone = module_clone.settings_instance
    assert area_settings_clone.pk != area_settings.pk
    assert area_settings_clone.polygon == area_settings.polygon
