import pytest
from django.core.urlresolvers import reverse

from adhocracy4.test.helpers import redirect_target
from adhocracy4.projects.models import Project


@pytest.mark.django_db
def test_project_list(client, organisation, project_factory, user, staff_user):
    project0 = project_factory(organisation=organisation)
    project1 = project_factory(organisation=organisation)

    project_list_url = reverse('a4dashboard:project-list', kwargs={
        'organisation_slug': organisation.slug})
    response = client.get(project_list_url)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(project_list_url)
    assert response.status_code == 403

    client.login(username=staff_user, password='password')
    response = client.get(project_list_url)
    assert response.status_code == 200

    project_list = response.context_data['project_list']
    assert list(project_list) == [project1, project0]


@pytest.mark.django_db
def test_blueprint_list(client, organisation, user, staff_user):
    blueprint_list_url = reverse('a4dashboard:blueprint-list', kwargs={
        'organisation_slug': organisation.slug})
    response = client.get(blueprint_list_url)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(blueprint_list_url)
    assert response.status_code == 403

    client.login(username=staff_user, password='password')
    response = client.get(blueprint_list_url)
    assert response.status_code == 200

    view = response.context_data['view']
    assert 1 == len(view.blueprints)
    assert 'questions' == view.blueprints[0][0]


@pytest.mark.django_db
def test_project_create(client, organisation, user, staff_user):
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

    client.login(username=staff_user, password='password')
    response = client.post(project_create_url, data)
    assert redirect_target(response) == 'project-edit'

    assert 1 == Project.objects.all().count()
    project = Project.objects.all().first()
    assert 'project name' == project.name
    assert 'project description' == project.description


@pytest.mark.django_db
def test_project_edit_redirect(client, project):
    project_edit_url = reverse('a4dashboard:project-edit', kwargs={
        'project_slug': project.slug})

    response = client.get(project_edit_url)
    assert response.status_code == 302
    assert response['location'].startswith('/dashboard')


@pytest.mark.django_db
def test_project_publish_perms(client, phase, user, staff_user):
    project = phase.module.project

    project_publish_url = reverse('a4dashboard:project-publish', kwargs={
        'project_slug': project.slug})

    data = {'action': 'publish'}

    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.post(project_publish_url, data)
    assert response.status_code == 403

    client.login(username=staff_user, password='password')
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'project-edit'


@pytest.mark.django_db
def test_project_publish(client, phase, staff_user):
    project = phase.module.project
    project.is_draft = True
    project.information = ''
    project.save()

    project_publish_url = reverse('a4dashboard:project-publish', kwargs={
        'project_slug': project.slug})

    data = {'action': 'publish'}

    # publishing incomplete projects has no effect
    client.login(username=staff_user, password='password')
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'project-edit'

    project.refresh_from_db()
    assert project.is_draft is True

    # complete project and publish it
    project.information = 'project information'
    project.save()

    client.login(username=staff_user, password='password')
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'project-edit'

    project.refresh_from_db()
    assert project.is_draft is False


@pytest.mark.django_db
def test_project_unpublish(client, phase, staff_user):
    project = phase.module.project
    project.is_draft = False
    project.save()

    project_publish_url = reverse('a4dashboard:project-publish', kwargs={
        'project_slug': project.slug})

    data = {'action': 'unpublish'}

    client.login(username=staff_user, password='password')
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'project-edit'

    project.refresh_from_db()
    assert project.is_draft is True

    # unpublishing draft projects has no effect
    client.login(username=staff_user, password='password')
    response = client.post(project_publish_url, data)
    assert redirect_target(response) == 'project-edit'

    project.refresh_from_db()
    assert project.is_draft is True


@pytest.mark.django_db
def test_project_publish_redirect(client, project, staff_user):
    project_publish_url = reverse('a4dashboard:project-publish', kwargs={
        'project_slug': project.slug})

    client.login(username=staff_user, password='password')

    response = client.post(project_publish_url, {'referrer': 'refurl'})
    assert response.status_code == 302
    assert response['location'] == 'refurl'

    response = client.post(project_publish_url, {}, HTTP_REFERER='refurl')
    assert response.status_code == 302
    assert response['location'] == 'refurl'

    response = client.post(project_publish_url, {})
    assert redirect_target(response) == 'project-edit'
